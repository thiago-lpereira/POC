from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)


notes = {
    0: "Germinare Tech - Confie no seu esforço e na sua preparação: cada desafio em DevOps é uma chance de mostrar o que você sabe e o quanto evoluiu. Vá com calma e com determinação, você consegue!",
    1: "Pipeline é VIDA - Confie no seu esforço e na sua preparação. Cada desafio é uma chance de mostrar o que você sabe e o quanto cresceu. Vá com calma, você consegue! ",
    2: "Cada passo na AWS Cloud é um avanço em direção à inovação e à eficiência. Confie no seu aprendizado e explore sem limites; o céu é o ponto de partida!"",
}


def note_repr(key):
    return {
        "url": request.host_url.rstrip("/") + url_for("notes_detail", key=key),
        "text": notes[key],
    }


@app.route("/", methods=["GET", "POST"])
def notes_list():
    """
    List or create notes.
    """
    if request.method == "POST":
        note = str(request.data.get("text", ""))
        idx = max(notes.keys()) + 1
        notes[idx] = note
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]


@app.route("/<int:key>/", methods=["GET", "PUT", "DELETE"])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == "PUT":
        note = str(request.data.get("text", ""))
        notes[key] = note
        return note_repr(key)

    elif request.method == "DELETE":
        notes.pop(key, None)
        return "", status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    app.run(debug=False)
