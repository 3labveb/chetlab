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
    'id': fields.Integer(required=True, description='disease id'),
    'disease': fields.String(required=True, description='disease'),
    'country': fields.String(required=True, description='country'),
    'recovered': fields.Integer(required=True, description='number of recovered'),
    'dead': fields.Integer(required=True, description='number of deaths'), 
    'arr': fields.List(fields.Raw,required=True, description='all list'),
})

# массив, который хранится в оперативной памяти
ls=[{"id": 0, "disease":"COVID-19", "country":"China", "recovered":100, "dead":3}]
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
        
        sick={"id":api.payload['id'], "disease": api.payload['disease'], "country": api.payload['country'], "recovered": api.payload['recovered'], "dead": api.payload['dead']} 

        ls.append(sick)
        # возвратить новый созданный массив клиенту
        return { 'array': ls}
# модель данные с двумя параметрами строкового типа
sortsc = api.model('lst', { 'array':fields.List(fields.Raw,required=True, description='all list')})
# url 127.0.0.1/list/mimmax
@name_space1.route("/getsortDisease")
class getsortDisease(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по заболеванию"""
        global ls
        dis=sorted(ls,key=lambda sick: sick['disease'])
        return {'array': dis}

@name_space1.route("/getsortCountry")
class getsortCountry(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по странам"""
        global ls
        cou=sorted(ls,key=lambda sick: sick['country'])
        return {'array': cou}

@name_space1.route("/getsortRecovered")
class getsortRecovered(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по выздоровевшим"""
        global ls
        rec=sorted(ls,key=lambda sick: sick['recovered'])
        return {'array': rec}

@name_space1.route("/getsortDead")
class getsortDead(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по умершим"""
        global ls
        dea=sorted(ls,key=lambda sick: sick['dead'])
        return {'array': dea}

@name_space1.route("/getsortId")
class getsortId(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по id"""
        global ls
        idi=sorted(ls,key=lambda sick: sick['id'])
        return {'array': idi}
oneval=api.model('one', {'val':fields.String}, required=True, description='one values')

#MAX
@name_space1.route("/getmaxDead")
class getmaxDead(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение максимального по умершим"""
        global ls
        mx=max([sick['dead'] for sick in ls ])
        return {'val': mx}

@name_space1.route("/getmaxRecovered")
class getmaxRecovered(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение максимального по выздоровевшим"""
        global ls
        mx=max([sick['recovered'] for sick in ls ])
        return {'val': mx}

#AVERAGE
@name_space1.route("/getaverDead")
class getaverDead(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение среднего по умершим"""
        global ls
        aver=sum([sick['dead'] for sick in ls ])/len(ls)
        return {'val': aver}

@name_space1.route("/getaverRecovered")
class getaverRecovered(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение среднего по выздоровевшим"""
        global ls
        aver=sum([sick['recovered'] for sick in ls ])/len(ls)
        return {'val': aver}

#MIN
@name_space1.route("/getminDead")
class getminDead(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение минимального по умершим"""
        global ls
        mn=min([sick['dead'] for sick in ls ])
        return {'val': mn}

@name_space1.route("/getminRecovered")
class getminRecovered(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение минимального по выздоровевшим"""
        global ls
        mn=min([sick['recovered'] for sick in ls ])
        return {'val': mn}

#REMOVING MAXIMUM DEATH
@name_space1.route("/deletemaxDead")
class deletemaxDead(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(list_)
    def get(self):
        """Удаление страны с максимальным количеством умерших"""
        global ls
        mx=max([sick['dead'] for sick in ls ])
        ls=[sick for sick in ls if sick['dead']!=mx]
        return { 'array': ls}
      
#STATISTICS
@name_space1.route("/changeStatistic")
class changeStatistic(Resource):
    @name_space1.doc("")
    # ожидаем на входе данных в соответствии с моделью list_
    @name_space1.expect(list_)
    # маршалинг данных в соответствии с list_
    @name_space1.marshal_with(list_)
    def patch(self):
        """Изменение статистики по заболеваниям"""
        global ls
        aver=sum([sick['recovered'] for sick in ls ])/len(ls)
        for sick in ls:
          if(sick["recovered"] >= aver):
            temp=sick["recovered"]/100*10
            sick["recovered"]=temp+sick["recovered"]
        return { 'array': ls}
    
#CHANGE COUNTRY DATA
@name_space1.route("/changedataCountry")
class changedataCountry(Resource):
    @name_space1.doc("")
    # ожидаем на входе данных в соответствии с моделью list_
    @name_space1.expect(list_)
    # маршалинг данных в соответствии с list_
    @name_space1.marshal_with(list_)
    def put(self):
        """Изменение данных по стране"""
        global ls
        for sick in ls:
          if(api.payload['country'] == sick["country"]):
            sick["id"] = api.payload['id']
            sick["disease"] = api.payload['disease']
            sick["recovered"] = api.payload['recovered']
            sick["dead"] = api.payload['dead']
        return { 'array': ls}
    
api.add_namespace(name_space1)

from flask_restplus import reqparse
from random import random

reqp = reqparse.RequestParser()
reqp.add_argument('id', type=int, required=False)

@name_space1.route("/chahgeDisease")
class chahgeDiseaseClass(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью reqp
    @name_space1.expect(reqp)
    @name_space1.marshal_with(list_)
    def get(self):
        """Удаление заболевания по id"""
        global ls
        args = reqp.parse_args()
        ls=[sick for sick in ls if sick['id']!=args['id']]
        return { 'array': ls}
    @name_space1.doc("")
    # ожидаем на входе данных в соответствии с моделью list_
    @name_space1.expect(list_)
    # маршалинг данных в соответствии с list_
    @name_space1.marshal_with(list_)
    def post(self):
        """Изменение заболевания по id"""
        global ls
        for sick in ls:
          if(api.payload['id'] == sick["id"]):
                sick["disease"] = api.payload['disease']
                sick["country"] = api.payload['country']
                sick["recovered"] = api.payload['recovered']
                sick["dead"] = api.payload['dead']
                return { 'array': ls}
        
        sick={"id":api.payload['id'], "disease": api.payload['disease'], "country": api.payload['country'], "recovered": api.payload['recovered'], "dead": api.payload['dead'] } 
        ls.append(sick)
        return ls
app.run(debug=True,host='127.0.0.1',port=5000)   
