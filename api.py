from flask import Flask, jsonify, request, render_template_string
import pyodbc
server="xxxx"
database="xxxx"
app = Flask(__name__)

def get_db_connection():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        return connection
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return None

def get_table_names():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        rows = cursor.fetchall()
        tables = [row.TABLE_NAME for row in rows]
        connection.close()
        return tables
    else:
        return []

@app.route('/')
def root():
    tables = get_table_names()
    html_content = '''
    <html>
    <head>
        <title>API de GYM</title>
        <script>
            function executeSQL() {
                var query = document.getElementById("sqlQuery").value;
                fetch('/execute_sql', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query }),
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("result").innerText = JSON.stringify(data, null, 2);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            }
            function viewTable() {
                var tableName = document.getElementById("tableSelect").value;
                var query = `SELECT * FROM ${tableName}`;
                document.getElementById("sqlQuery").value = query;
                executeSQL();
            }
        </script>
    </head>
    <body>
        <h1>API de GYM</h1>
        <button onclick="window.location.href='/version'">Obtener Versión de SQL Server</button><br><br>
        <button onclick="window.location.href='/tables'">Obtener Tablas</button><br><br>
        <h2>Ver todo de</h2>
        <select id="tableSelect">
            {% for table in tables %}
                <option value="{{ table }}">{{ table }}</option>
            {% endfor %}
        </select>
        <button onclick="viewTable()">Ver</button><br><br>
        <h2>Consola SQL</h2>
        <textarea id="sqlQuery" rows="4" cols="50">SELECT * FROM </textarea><br>
        <button onclick="executeSQL()">Ejecutar</button>
        <pre id="result"></pre>
    </body>
    </html>
    '''
    return render_template_string(html_content, tables=tables)

@app.route('/version', methods=['GET'])
def get_sql_version():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        connection.close()
        return jsonify({"sql_version": row[0]})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

@app.route('/tables', methods=['GET'])
def get_tables():
    tables = get_table_names()
    return jsonify({"tables": tables})

@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    data = request.get_json()
    query = data.get('query')
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                results = [dict(zip(columns, row)) for row in rows]
                connection.close()
                return jsonify({"results": results})
            else:
                connection.commit()
                connection.close()
                return jsonify({"message": "Query executed successfully"})
        except Exception as ex:
            connection.close()
            return jsonify({"error": str(ex)}), 400
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

if __name__ == '__main__':
    app.run(debug=True)
