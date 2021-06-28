  
from flask import Flask, Blueprint
from flask_restplus import Api, Resource
app = Flask(__name__)
api = Api(app = app)
# описание главного блока нашего api http://127.0.0.1:5000/main/.
name_space = api.namespace('main', description='Main APIs')
@name_space.route("/")
class MainClass(Resource):
    def get(self):
        return {"status": "Got new data"}
    def post(self):
        return {"status": "Posted new data"}
    def patch(self):
        return {"status": "Patched new data"}
    def put(self):
        return {"status": "Put new data"}  

from flask_restplus import fields
# определение модели данных массива
list_ = api.model('list', {
    'code': fields.Integer(required=True, description='product code'),
    'store': fields.String(required=True, description='store'),
    'manufacturer': fields.String(required=True, description='manufacturer of product'),
    'price': fields.Integer(required=True, description='the price of thr product'),
    #через сколько дней закончиться срок годности
    'suitability': fields.Integer(required=True, description='time to expiration date'), 
    'arr': fields.List(fields.Raw,required=True, description='all list'),
})

# массив, который хранится в оперативной памяти
ls=[{"code": 35463, "store":"Yarche", "manufacturer":"Baltor", "price":456, "suitability":21}]
universalID=int(0)
allarray = ls
name_space1 = api.namespace('list', description='list APIs')

@name_space1.route("/ListClass")
class ListClass(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(list_)
    def get(self):
        """Получение всего хранимого массива"""
        global ls
        return ls
    @name_space1.doc("")
    # ожидаем на входе данных в соответствии с моделью list_
    @name_space1.expect(list_)
    # маршалинг данных в соответствии с list_
    @name_space1.marshal_with(list_)
    def post(self):
        """Создание массива"""
        global allarray
        # получить переданный массив из тела запроса
        
        sick={"code":api.payload['code'], "store": api.payload['store'], "manufacturer": api.payload['manufacturer'], "price": api.payload['price'], "suitability": api.payload['suitability']} 

        ls.append(sick)
        # возвратить новый созданный массив клиенту
        return { 'array': ls}
# модель данные с двумя параметрами строкового типа
sortsc = api.model('lst', { 'array':fields.List(fields.Raw,required=True, description='all list')})
# url 127.0.0.1/list/mimmax
@name_space1.route("/getsortCode")
class getsortCode(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по коду"""
        global ls
        cod=sorted(ls,key=lambda sick: sick['code'])
        return {'array': cod}
    
@name_space1.route("/getsortStore")
class getsortStore(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по названию магазина"""
        global ls
        str=sorted(ls,key=lambda sick: sick['store'])
        return {'array': str}

@name_space1.route("/getsortManufacturer")
class getsortManufacturer(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по производителям"""
        global ls
        man=sorted(ls,key=lambda sick: sick['manufacturer'])
        return {'array': man}

@name_space1.route("/getsortprice")
class getsortPrice(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по цене"""
        global ls
        prc=sorted(ls,key=lambda sick: sick['price'])
        return {'array': prc}

@name_space1.route("/getsortSuitability")
class getsortSuitability(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по времени до окончания срока годности"""
        global ls
        stb=sorted(ls,key=lambda sick: sick['suitability'])
        return {'array': stb}

oneval=api.model('one', {'val':fields.String}, required=True, description='one values')

#MAX
@name_space1.route("/getmaxSuitability")
class getmaxSuitability(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение максимального по времени до истечения срока годности"""
        global ls
        mx=max([sick['suitability'] for sick in ls ])
        return {'val': mx}

@name_space1.route("/getmaxPrice")
class getmaxPrice(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение максимального по цене"""
        global ls
        mx=max([sick['price'] for sick in ls ])
        return {'val': mx}

#AVERAGE
@name_space1.route("/getaverSuitability")
class getaverSuitability(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение среднего по времени до истечения срока годности"""
        global ls
        aver=sum([sick['suitability'] for sick in ls ])/len(ls)
        return {'val': aver}

@name_space1.route("/getaverPrice")
class getaverPrice(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение среднего по цене"""
        global ls
        aver=sum([sick['price'] for sick in ls ])/len(ls)
        return {'val': aver}
      
@name_space1.route("/changeaverPrice")
class changeaverPrice(Resource):
    @name_space1.doc("")
    # маршалинг данных в соответствии с list_
    @name_space1.marshal_with(list_)
    def patch(self):
        """Изменение цены товара цена которого больше средней на 10 процентов"""
        global ls
        chaver=sum([sick['price'] for sick in ls ])/len(ls)
        for sick in ls:
          if(sick["price"] >= chaver):
            temp=sick["price"]/100*10
            sick["price"]=temp+sick["price"]
        return { 'array': ls}      

#MIN
@name_space1.route("/getminSuitability")
class getminSuitability(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение минимального по времени до истечения срока годности"""
        global ls
        mn=min([sick['suitability'] for sick in ls ])
        return {'val': mn}

@name_space1.route("/getminPrice")
class getminPrice(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение минимального по цене"""
        global ls
        mn=min([sick['price'] for sick in ls ])
        return {'val': mn}
      
@name_space1.route("/changeminPrice")
class changeminPrice(Resource):
    @name_space1.doc("")
    @name_space1.expect(list_)
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(list_)
    def put(self):
        """Изменение товара минимального по цене"""
        global ls
        mn=min([sick['price'] for sick in ls ])
        for sick in ls:
          if(sick["price"]==mn):
            sick["code"] = api.payload['code']
            sick["store"] = api.payload['store']
            sick["manufacturer"] = api.payload['manufacturer']
            sick["price"] = api.payload['price']
            sick["suitability"] = api.payload['suitability']
        return {'array': ls}
      
@name_space1.route("/deleteminPrice")
class deleteminPrice(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(list_)
    def get(self):
        """Удаление товара с минимальной ценой"""
        global ls
        mnp=min([sick['price'] for sick in ls ])
        ls=[sick for sick in ls if sick['price']!=mnp]
        return { 'array': ls}
      
api.add_namespace(name_space1)

from flask_restplus import reqparse
from random import random

reqp = reqparse.RequestParser()
reqp.add_argument('code', type=int, required=False)

@name_space1.route("/chahgePrice")
class chahgePriceClass(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью reqp
    @name_space1.expect(reqp)
    @name_space1.marshal_with(list_)
    def get(self):
        """Удаление товара по коду"""
        global ls
        args = reqp.parse_args()
        ls=[sick for sick in ls if sick['code']!=args['code']]
        return { 'array': ls}
    @name_space1.doc("")
    # ожидаем на входе данных в соответствии с моделью list_
    @name_space1.expect(list_)
    # маршалинг данных в соответствии с list_
    @name_space1.marshal_with(list_)
    def post(self):
        """Изменение товара по коду"""
        global ls
        for sick in ls:
          if(api.payload['code'] == sick["code"]):
                sick["store"] = api.payload['store']
                sick["manufacturer"] = api.payload['manufacturer']
                sick["price"] = api.payload['price']
                sick["suitability"] = api.payload['suitability']
                return { 'array': ls}
        
        sick={"code":api.payload['code'], "store": api.payload['store'], "manufacturer": api.payload['manufacturer'], "price": api.payload['price'], "suitability": api.payload['suitability'] } 
        ls.append(sick)
        return ls
app.run(debug=True,host='127.0.0.1',port=5000)   
