from flask import Flask, render_template

import pygal

import psycopg2

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     x = 1000
#     return render_template("My4thwebsite.html", x=x)
#
# @app.route('/About')
# def About_page():
#     return render_template("About.html")

@app.route('/xyz')
def piechart():
    conn = psycopg2.connect("dbname='salesdemo' user='postgres' host='localhost' password='Ann@2020'")

    cur1 = conn.cursor()

    cur1.execute("""SELECT type, count (type)
FROM public.inventories
group by inventories.type
""")

    records = cur1.fetchall()

    # print(type(records))

    for each in records:
        print(each)


    ratios = [("Gentlement", 5), ("Ladies", 9)]
    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('Products', records[0][1])
    pie_chart.add('Others', records[1][1])
    pie_chart.add('Services', records[2][1])
    # pie_chart.add('Chrome', 36.3)
    # pie_chart.add('Safari', 4.5)
    # pie_chart.add('Opera', 2.3)
    pie_data = pie_chart.render_data_uri()

    cur = conn.cursor()

    cur.execute("""SELECT to_char(to_timestamp(date_part('month',sales.ceated_at)::text,'MM'),'Month') as month, round(sum(inventories.selling_price*sales.quantity))
from public.inventories 
join sales on sales.inv_id = inventories.id
group by extract (month from sales.ceated_at)
order by extract (month from sales.ceated_at) asc
""")
    rows = cur.fetchall()

    # print(type(rows))

    months = []
    totalsales = []

    for each in rows:
        months.append(each[0])
        totalsales.append(each[1])
    print(months)
    print(totalsales)

    graph = pygal.Line()
    graph.title = '% Change Coolness of programming languages over time.'

    graph.x_labels = months
    graph.add('Total Sales', totalsales)
    # graph.add('Java', [15, 45, 76, 80, 91, 95])
    # graph.add('C++', [5, 51, 54, 102, 150, 201])
    # graph.add('All others combined!', [5, 15, 21, 55, 92, 105])
    graph_data = graph.render_data_uri()

    return render_template('xyz.html', pie_data = pie_data, graph_data = graph_data)


if __name__ == '__main__':
    app.run()