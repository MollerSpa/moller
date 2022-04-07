from odoo import api, fields, models
import requests
from ..models.vex_soluciones_meli_config  import API_URL, INFO_URL, get_token
import logging
_logger = logging.getLogger(__name__)
import pprint
import base64
from odoo.addons.payment.models.payment_acquirer import ValidationError

id_api       = 'id_vex'
server_api   = 'server_vex'
class MeliActionSynchro(models.TransientModel):
    _inherit       = "vex.synchro"
    server_meli    = fields.Many2one('meli.synchro.instance',"Instance")

    @api.model
    def check_terminos(self, t, server, atr):
        # sincronizar todos los terminos
        # buscar el id  del termino
        t_id = None
        existe = self.env['product.attribute.value'].search(
            [('name', '=', str(t)), (server_api, '=', int(server.id)), ('attribute_id', '=', int(atr.id))])
        if existe:
            t_id = existe
        return t_id
    @api.model
    def inser_terminos(self, term, atributo, server):
        # import json
        # y = json.dumps(term)
        for t in term:
            et = self.env['product.attribute.value'].search([('name', '=', str(t['name'])),
                                                             (server_api, '=', server.id),
                                                             ('attribute_id', '=', atributo.id)])
            if not et:
                data = {
                    'name': "'"+str(t['name'])+"'",
                    id_api: "'"+str(t['id'])+"'",
                    server_api: server.id,
                    'attribute_id': atributo.id
                }
                self.json_execute_create('product.attribute.value', data)

    @api.model
    def check_attributes(self, at, server):
        at_id = None
        existe = self.env['product.attribute'].search([(id_api, '=', str(at['id'])), (server_api, '=', int(server.id))])
        if not existe:
            # json = self.json_fields(attr, 'products/attributes', wcapi,server)
            # raise ValidationError(json['create']['server'])
            data = {
                'name': "'"+str(at['name'])+"'",
                id_api: "'"+str(at['id'])+"'",
                server_api: server.id,
                'create_variant': "'no_variant'",
                'display_type': "'radio'",
                'conector': "'meli'"
            }
            self.json_execute_create('product.attribute',data)
        # insertar sus terminod

        # raise
        existe = self.env['product.attribute'].search([(id_api, '=', str(at['id'])), (server_api, '=', int(server.id))])
        self.inser_terminos(at['values'], existe , server)
        return existe

    def check_synchronize(self,server):
        res = super(MeliActionSynchro, self).check_synchronize(server)
        if server.conector == 'meli':
            access_token = server.access_token
            res = requests.get(INFO_URL, params={'access_token': access_token})

            if res.status_code != 200:
                token = get_token(server.app_id, server.secret_key, server.redirect_uri, '', server.refresh_token)
                if token:
                    update = {
                        'access_token' : token['access_token'],
                        'refresh_token' : token['refresh_token'],
                    }
                    #exist = self.env['meli.synchro.instance'].search([('user_id', '=', str(server.user_id))])
                    server.write(update)
        return res

    def start_import(self):
        res = super(MeliActionSynchro, self).start_import()
        if self.conector == 'meli':
            server = self.server_vex
            id_action = 'odoo-mercadolibre.action_view_meli_synchro'
            return self.vex_import(server,id_action,None)
        return res

    @api.model
    def insert_variations(self, dr, server, creado):
        # recorrer las variantes y chekar todas los atrbutos
        # guardar el id por atributo y luego colocarlo en el respect
        variantes_array = {'ja'}
        values_array = {'ja'}
        #obtener las variantes
        variants = dr['variations']
        if variants:
            #bucle a las variantes
            for v in variants:
                #raise ValidationError(v['id'])
                # buscar si existe una variante con los atributo
                ppp = self.env['product.product'].search([('product_tmpl_id', '=', int(creado.id)),

                                                          ('id_vex_varition', '=', str(v['id']))])

                #array  para guardar los value ids
                data_values_ids = []
                for vi in v['attribute_combinations']:
                    #verificar el atributo 
                    at = self.check_attributes(vi, server)
                    #raise ValidationError(at)
                    variantes_array.add(at.id)
                    json_at = []
                    if at:
                        # buscar si existe el atributo en atribute line
                        atl = self.env['product.template.attribute.line'].search(
                            [('attribute_id', '=', int(at.id)), ('product_tmpl_id', '=', int(creado.id))])
                        #raise ValidationError(atl)
                        if atl:
                            # verificar si existe ese valor  en ese atributo line
                            valores_actuales = atl.value_ids
                            #raise ValidationError(valores_actuales)
                            va_array = []
                            for va in valores_actuales:
                                va_array.append(va.name)
                            #raise ValidationError(va_array)

                            for vx in vi['values']:
                                # raise ValidationError(vx)
                                vv = None
                                if not vx['name'] in va_array:
                                    #raise ValidationError(vx['name'])
                                    vv = self.check_terminos(vx['name'], server, at)
                                    # raise ValidationError('que')
                                    if vv:
                                        atl.value_ids += vv

                                else:
                                    vv = self.check_terminos(vx['name'], server, at)
                                    #raise ValidationError(vv)
                                if vv:
                                    line_v = self.env['product.template.attribute.value'].search(
                                        [('product_attribute_value_id', '=', vv.id), ('attribute_id', '=', at.id),
                                         ('product_tmpl_id', '=', creado.id),
                                         ('attribute_line_id', '=', atl.id)])
                                    data_values_ids.append(line_v.id)

                                values_array.add(str(at.id) + '_' + vx['name'])
                        else:
                            for vx in vi['values']:
                                vv = self.check_terminos(vx['name'], server, at)
                                json_at.append(vv.id)
                            '''
                            creado.attribute_line_ids += self.env['product.template.attribute.line'].new({
                                'attribute_id': int(at.id),
                                'value_ids': [(6, 0, json_at)]
                            })
                            '''
                            data = {
                                'active': "'t'",
                                'attribute_id': int(at.id),
                                'product_tmpl_id': int(creado.id)
                            }
                            self.json_execute_create('product.template.attribute.line',data)
                            #currents = self._cr.dictfetchall()
                            #raise ValidationError(currents)
                            line = self.env['product.template.attribute.line'].search([('product_tmpl_id', '=', creado.id),('attribute_id', '=', at.id)])
                            #raise ValidationError(line)

                            for jt in json_at:
                                # raise ValidationError(insert_value)
                                insert_tmp_values = "INSERT INTO  product_template_attribute_value " \
                                                    "(ptav_active,product_attribute_value_id,attribute_line_id," \
                                                    "product_tmpl_id,attribute_id)" \
                                                    " VALUES " \
                                                    "('t',{},{},{},{}) ON CONFLICT DO NOTHING".format(jt, line.id,
                                                                                                   creado.id,at.id)
                                self.env.cr.execute(insert_tmp_values)
                                line_v = self.env['product.template.attribute.value'].search(
                                    [('product_attribute_value_id', '=', jt), ('attribute_id', '=', at.id),('product_tmpl_id','=',creado.id),
                                     ('attribute_line_id','=',line.id)])
                                data_values_ids.append(line_v.id)
                                # insertar values
                                '''
                                insert_value = "INSERT INTO product_attribute_value_product_template_attribute_line_rel " \
                                               "(product_attribute_value_id,product_template_attribute_line_id) " \
                                               "VALUES " \
                                               "({},{}) ON CONFLICT DO NOTHING".format(jt, line.id)
                                self.env.cr.execute(insert_value)
                                '''

                #raise ValidationError(ppp)
                url = ''
                pictures = dr['pictures']
                for p in pictures:
                    if p['id'] == v['picture_ids'][0]:
                        url = p['url']
                #raise ValidationError(url)
                myimage = requests.get(url)
                #raise ValidationError(ppp)

                if not ppp:
                    #raise ValidationError('porque')
                    create = {
                        'active': "'t'",
                        'product_tmpl_id': creado.id,
                        'id_vex_varition': "'"+str(v['id'])+"'",
                        'vex_regular_price': v['price']
                    }
                    sql_fields = self.sql_fields('product.product', {'create': create}, v['id'], None)
                    self.env.cr.execute(sql_fields['create'])
                    ppp = self.env['product.product'].search([('product_tmpl_id', '=', int(creado.id)),
                                                              ('id_vex_varition', '=', str(v['id']))])
                    ppp.write({'image_1920': base64.b64encode(myimage.content)})
                    for g in data_values_ids:
                        query_combi = "INSERT INTO product_variant_combination " \
                                      "(product_product_id,product_template_attribute_value_id) VALUES" \
                                      "({},{}) ON CONFLICT DO NOTHING".format(ppp.id, g)
                        self.env.cr.execute(query_combi)
                #raise ValidationError(ppp)
                dt = {'id_vex_varition': "'"+str(v['id'])+"'", 'vex_regular_price': v['price']}
                self.json_execute_update('product.product',dt, ppp.id)
                #self.env.cr.execute(query_combi)


                #raise ValidationError(data_values_ids)
                #dele = "DELETE FROM product_variant_combination WHERE product_product_id = "+str(ppp.id)
                #self.env.cr.execute(dele)



                    #raise ValidationError(self._cr.dictfetchall())

                '''

                indices = ",".join([str(elem) for elem in data_values_ids])
                if indices != '':
                    q_update_variation = "UPDATE product_product SET " \
                                         "combination_indices = '{}' WHERE " \
                                         "id = {}".format(indices, ppp.id)
                    try:
                        self.env.cr.execute(q_update_variation)
                    except:
                        a = 1

                '''
                # verificar el producto product creado
            # self.insert_variants(variants,dr['pictures'],creado,server)

            # depurar las variantes eliminadas
            '''
            variantes_odoo_array = {'ja'}
            for ii in creado.attribute_line_ids:
                variantes_odoo_array.add(ii.attribute_id.id)
            resta = variantes_odoo_array - variantes_array
            for r in resta:
                self.env['product.template.attribute.line'].search([('attribute_id', '=', int(r)),('product_tmpl_id','=',creado.id)]).unlink()

            interseccion = variantes_odoo_array & variantes_array
            interseccion.remove('ja')
            for i in interseccion:
                ii = self.env['product.template.attribute.line'].search([('attribute_id.id', '=', int(i))
                                                                            ,('product_tmpl_id','=',creado.id)])
                #depurar los valores que no coinciden
                if ii:
                    valores_odoo =  {'ja'}
                    for va in ii.value_ids:
                        valores_odoo.add(str(va.attribute_id.id)+'_'+va.name)
                    #if creado.id == 356 :
                    #    raise ValidationError(values_array)
                    resta = valores_odoo - values_array
                    if creado.id == 356 :
                            _logger.info('Valores Iniciales: %s', pprint.pformat(values_array))
                            _logger.info('Valores Finales: %s', pprint.pformat(valores_odoo))
                            #raise ValidationError(resta)
                    #resta.remove('ja')
                    for r in resta:
                        split = r.split('_')
                        split = split[1]

                        for x in ii.value_ids:
                            if x.name == split:
                                ii.value_ids = [(3,x.id)]
                                #if creado.id == 356 :
                                #    raise ValidationError(x)
                        d = self.env['product.attribute.value'].search([('attribute_id', '=', int(ii.id)),('name','=',str(r))])

                        d.unlink()
            '''
        else:
            #crear product de template
            ppp = self.env['product.product'].search([('product_tmpl_id', '=', int(creado.id)),

                                                      ('id_vex_varition', '=', str(creado.id))])
            if not ppp:
                create = {
                   'active': "'t'",
                    'product_tmpl_id': creado.id,
                    'id_vex_varition': "'" + str(creado.id) + "'",
                    #'vex_regular_price': v['price']
                }
                self.json_execute_create('product.product', create)


        return 0

    @api.model
    def check_imagenes(self, imagenes, server, exist):
        # verificar las imagenes
        import json

        imagenes_array = {'ja'}

        for i in imagenes:
            imm = self.check_picture(i, server, exist)
            imagenes_array.add(imm.id)
            imagenes_odoo_array = {'ja'}
            for ii in exist.product_template_image_ids:
                imagenes_odoo_array.add(ii.id)
            resta = imagenes_odoo_array - imagenes_array
            for r in resta:
                self.env['product.image'].search([('id', '=', int(r))]).unlink()


    @api.model
    def check_picture(self, image, server, product):

        # verificar si la imagen existe
        img = product.product_template_image_ids.search([(id_api, '=', image['id']),
                                                         (server_api, '=', server.id)
                                                         ], limit=1)
        if not img:
            url = image['url']
            myfile = requests.get(url)
            img = self.env['product.image'].create({
                id_api: image['id'],
                server_api: server.id,
                'conector': server.conector,
                'image_1920': base64.b64encode(myfile.content),
                'product_tmpl_id': product.id,
                'name': image['id'],

            })
            #raise ValidationError(product)
        return img

        return 0

