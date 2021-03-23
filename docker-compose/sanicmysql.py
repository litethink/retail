# coding:utf-8

from sanic import Sanic
from sanic import response

from sanicdb import SanicDB

app = Sanic('test')
db = SanicDB('localhost', 'retail001', 'retail001', '001retail', sanic=app)


@app.route('/db/test')
async def dbTest(request):
    sql = 'select * from students where age=18'
    data = await app.db.query(sql)
    return response.json(data)


if __name__ == '__main__':
    app.run()

