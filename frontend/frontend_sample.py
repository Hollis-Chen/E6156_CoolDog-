from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display_string():
    user_string = None
    if request.method == 'POST':
        user_string = request.form.get('input_string')
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>String Display</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="row">
                    <div class="col-md-6 offset-md-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Enter a String</h5>
                                <form method="post">
                                    <div class="form-group">
                                        <input type="text" name="input_string" class="form-control" placeholder="Enter your string" required>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Submit</button>
                                </form>
                                {% if user_string %}
                                <hr>
                                <p>You entered: <strong>{{ user_string }}</strong></p>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''', user_string=user_string)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

