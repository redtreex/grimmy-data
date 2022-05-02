from flask import Flask, render_template, request, make_response
from data_cleaner import data_cleaner
import pandas as pd

result_file = ''
result_file_desc = ''
app = Flask(__name__, template_folder='templates', static_folder='static')
dc = data_cleaner()


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        up_files = request.files.getlist('file')
        dedup = request.form.get('rem_dup')
        rem_null = request.form.get('rem_null')
        scale = request.form.get('scale')
        result = {}
        task = {
            'dedup': True if dedup == 'True' else False,
            'rem-null': True if rem_null == 'True' else False,
            'scale': True if scale == 'True' else False
        }
        if up_files[1].filename == '':
            csv_1 = pd.read_csv(up_files[0])
            result = dc.clean_data(task, [csv_1])
        else:
            csv_1 = pd.read_csv(up_files[0])
            csv_2 = pd.read_csv(up_files[1])
            result = dc.clean_data(task, [csv_1, csv_2])

        global result_file
        result_file = result['file']
        global result_file_desc
        result_file_desc = result['desc']

        #  testing the html render
        first_half = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../static/styles/file-down-dash.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Roboto:wght@300;400;500&display=swap"
        rel="stylesheet">
    <link rel="shortcut icon" href="../static/img/favicon.png" type="image/png">
    <title>Grimy Data</title>
</head>

<body>
    <header>
        <div id="logo-text-div">
            <a href="http://localhost/recent/pages/file-up-dash.php">Grimy<span>Data</span></a>
        </div>
        <div id="link-div">
            <div id="link-wrapper">
                <!-- Back to dashboard URL -->
                <a href="http://grimydata.epizy.com/pages/file-up-dash.php">Back</a>
                <!-- Logout to Login Page -->
                <a href="http://grimydata.epizy.com/pages/logout.php">Log out</a>
            </div>
        </div>
    </header>

    <div id="wrapper">
        <div id="table-div">
            <div id="table-meta">
                <h4>Statistical Informations of the file(s)</h2>
                    <!-- Download button for the table -->
                    <!-- Download Result file description api  -->
                    <a href="https://grimy-data.herokuapp.com/download_result_file_desc"><button>Download</button></a>
            </div>"""
        second_half = """</div>
        <div id="download-div">
            <h3>Your File is Ready To Download</h3>
            <!-- Final Download Button -->
            <!-- Download file api location -->
            <a href="https://grimy-data.herokuapp.com/download_result_file"><button id="download-btn">Download</button></a>
        </div>
    </div>

    <footer>
        <p>2022 All rights reserved | CSE391</p>
    </footer>

</body>

</html>"""
        df_html = first_half + "\n" + result_file_desc.to_html(float_format='%.3f', table_id='desc-table',
                                                               border=0) + "\n" + second_half

        text_file = open("./templates/file-down-dash.html", "w")
        text_file.write(df_html)
        text_file.close()

        #  return the file download dashboard
        return render_template('file-down-dash.html')


@app.route('/download_result_file', methods=['GET'])
def download_result_file():
    if request.method == 'GET':
        resp = make_response(result_file.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=cleaned_file.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route('/download_result_file_desc', methods=['GET'])
def download_result_desc_file():
    if request.method == 'GET':
        resp = make_response(result_file_desc.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=file_statistics.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


if __name__ == '__main__':
    app.run(port=5002)
