from flask import Flask, jsonify, render_template
from flask import request, Blueprint

app = Flask(__name__, static_url_path='/static')
json_bp = Blueprint('jsonpelis', __name__)

@json_bp .route('/getPeliculas', methods=['GET'])
def getPeliculas():
    try:
        if request.method == 'GET':
            retorno = {
                "categoria": [
                    {
                        "nombre": "Aventura",
                        "peliculas": {
                            "pelicula": [
                                {
                                    "titulo": "Las momias del faraon",
                                    "director": "Luc Besson",
                                    "anio": "2010",
                                    "fecha": "2023-02-05",
                                    "hora": "19:30",
                                    "imagen": "https://es.web.img2.acsta.net/medias/nmedia/18/78/77/56/19477844.jpg",
                                    "precio": "52"
                                },
                                 {
                                    "titulo": "Dragon Ball Super Hero",
                                    "director": "Tetsuro Kodama",
                                    "anio": "2022",
                                    "fecha": "2023-07-07",
                                    "hora": "21:15",
                                    "imagen": "https://pics.filmaffinity.com/Dragon_Ball_Super_Super_Hero-181561937-large.jpg",
                                    "precio": "90"
                                },
                                {
                                    "titulo": "Dragon Ball Super Broly",
                                    "director": "Tatsuya Nagamine",
                                    "anio": "2018",
                                    "fecha": "2023-08-07",
                                    "hora": "21:15",
                                    "imagen": "https://es.web.img3.acsta.net/pictures/18/12/18/13/00/2556818.jpg",
                                    "precio": "90"
                                },
                                {
                                    "titulo": "Super Mario Bros",
                                    "director": "Luis Leonardo Suarez",
                                    "anio": "2023",
                                    "fecha": "2023-08-07",
                                    "hora": "21:15",
                                    "imagen": "https://www.universalpictures-latam.com/tl_files/content/movies/super_mario_bros/posters/05.jpg",
                                    "precio": "90"
                                },
                                {
                                    "titulo": "Aladdin",
                                    "director": "Chad Stahelski",
                                    "anio": "2019",
                                    "fecha": "2023-06-06",
                                    "hora": "20:00",
                                    "imagen": "https://m.media-amazon.com/images/M/MV5BMjQ2ODIyMjY4MF5BMl5BanBnXkFtZTgwNzY4ODI2NzM@._V1_FMjpg_UX1000_.jpg",
                                    "precio": "55"
                                }
                            ]
                        }
                    },
                    {
                        "nombre": "Infantil",
                        "peliculas": {
                            "pelicula": [
                                {
                                    "titulo": "Sing 2",
                                    "director": "Garth Jenningsr",
                                    "anio": "2021",
                                    "fecha": "2023-04-05",
                                    "hora": "14:30",
                                    "imagen": "https://www.universalpictures.com.ar/tl_files/content/movies/sing2/posters/01.jpg",
                                    "precio": "75"
                                },
                                {
                                    "titulo": "spirited away",
                                    "director": "Hayao Miyazaki",
                                    "anio": "2001",
                                    "fecha": "2023-07-07",
                                    "hora": "21:15",
                                    "imagen": "https://cinematecadebogota.gov.co/sites/default/files/styles/318_x_460/public/afiches/screen_shot_2021-07-30_at_4.18.59_pm.png?itok=9pijB2o2",
                                    "precio": "82"
                                }
                            ]
                        }
                    }
                ]
            }
            return jsonify(retorno)
        else:
            retorno = {'mensaje': 'Error en la petición, método incorrecto'}
        return jsonify(retorno)
    except:
        return {"mensaje": "Error interno en el servidor", "status": 500}

@json_bp .route('/peliculas_j')
def peliculas():
    data = getPeliculas().json
    return render_template('pelis.html', data=data)


app.register_blueprint(json_bp)

if __name__ == '__main__':
    app.run()
