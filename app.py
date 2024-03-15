from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulação de dados de usuário (substituir por um sistema de autenticação real)
users = {}

# Dados simulados para o aplicativo de saúde
health_data = {}

# Estrutura para informações adicionais do usuário
user_profiles = {}

# Adicione uma nova chave para armazenar os usuários autenticados
authenticated_users = set()

# tela de Inicio


@app.route("/")
def welcome():
    return render_template("welcome.html")


# Médias de calorias por hora para cada exercício


calories_per_hour = {
    "Pular corda": 1074,
    "Corrida (12 km/h)": 1074,
    "Taekwondo": 937,
    "Natação (ritmo intenso)": 892,
    "Subir degraus": 819,
    "Corrida (8 km/h)": 755,
    "Basquete": 728,
    "Futebol americano": 728,
    "Tênis": 728,
    "Patinação": 683,
    "Aeróbica (alto impacto)": 664,
    "Mochilão (com trilha)": 637,
    "Patinação no gelo": 637,
    "Squash": 637,
    "Esqui": 619,
    "Trilha": 546,
    "Remo (na máquina)": 546,
    "Esqui aquático": 546,
    "Natação (ritmo leve ou moderado)": 528,
    "Hidroginástica": 501,
    "Aeróbica (baixo impacto)": 455,
    "Aparelho elíptico (moderado)": 455,
    "Levantamento de peso": 455,
    "Softbol ou basebol": 455,
    "Golfe (carregando os tacos)": 391,
    "Esqui (descida)": 391,
    "Caminhada (6 km/h)": 391,
    "Ciclismo (leve, por lazer)": 364,
    "VoIei": 364,
    "PowerYoga": 364,
    "Canoagem": 319,
    "Boliche": 273,
    "Dança de Salão": 273,
    "Tai chi": 273,
    "Caminhada (4 km/h)": 255,
    "Hatha Yoga": 228,
}


def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 2) if height != 0 else 0


def classify_imc(imc):
    # Adicione sua lógica para classificar o IMC em diferentes categorias
    # Este é apenas um exemplo simples
    if imc < 18.5:
        return "Abaixo do Peso"
    elif 18.5 <= imc < 24.9:
        return "Peso Normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidade"


@app.route("/")
def home():
    return redirect(url_for("login"))

# Rota de cadastro


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        health_goals = request.form.get("health_goals")
        sex = request.form.get("sex")
        age = int(request.form.get("age", 0))

        # Crie um perfil para o novo usuário com informações adicionais
        user_profiles[username] = {
            "age": age,
            "sex": sex,
            "health_goals": health_goals,
            "exercise_log": []
        }

        # Adicione o novo usuário aos dados simulados
        users[username] = {"password": password, "name": username}

        return redirect(url_for("login"))

    return render_template("cadastro.html")

# Rota para a tela de login


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username]["password"] == password:
            authenticated_users.add(username)
            return redirect(url_for("dashboard", username=username))
        else:
            return render_template("login.html", error="Credenciais inválidas")

    return render_template("login.html")

# Rota do dashboard


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    if username not in authenticated_users:
        return redirect(url_for("login"))

    user_profile = user_profiles.get(
        username, {"age": 0, "sex": "", "health_goals": "", "exercise_log": []})

    if request.method == "POST":
        if "calculate_imc" in request.form:
            weight = float(request.form.get("weight", 0))
            height = float(request.form.get("height", 0))
            user_profile["imc"] = calculate_bmi(weight, height)

        elif "exercise_type" in request.form:
            exercise_type = request.form.get("exercise_type")
            duration = int(request.form.get("duration", 0))

            if exercise_type and duration > 0:
                calories_per_hour = get_calories_per_hour(exercise_type)
                calories_burned = calculate_calories_burned(
                    calories_per_hour, duration)

                user_profile["exercise_log"].append({
                    "type": exercise_type,
                    "duration": duration,
                    "calories_burned": calories_burned
                })

    return render_template("dashboard.html", username=username, user_profile=user_profile, classify_imc=classify_imc)


# Função para obter as calorias por hora com base no tipo de exercício


def get_calories_per_hour(exercise_type):
    # Adicione as médias de calorias por hora para cada exercício
    calories_mapping = {
        "Pular corda": 1074,
        "Corrida (12 km/h)": 1074,
        "Tae kwon do": 937,
        "Natação (ritmo intenso)": 892,
        "Subir degraus": 819,
        "Corrida (8 km/h)": 755,
        "Basquete": 728,
        "Futebol americano": 728,
        "Tênis": 728,
        "Patinação": 683,
        "Aeróbica (alto impacto)": 664,
        "Mochilão (com trilha)": 637,
        "Patinação no gelo": 637,
        "Squash": 637,
        "Esqui": 619,
        "Trilha": 546,
        "Remo (na máquina)": 546,
        "Esqui aquático": 546,
        "Natação (ritmo leve ou moderado)": 528,
        "Hidroginástica": 501,
        "Aeróbica (baixo impacto)": 455,
        "Aparelho elíptico (moderado)": 455,
        "Levantamento de peso": 455,
        "Softbol ou basebol": 455,
        "Golfe (carregando os tacos)": 391,
        "Esqui (descida)": 391,
        "Caminhada (6 km/h)": 391,
        "Ciclismo (leve, por lazer)": 364,
        "VoIei": 364,
        "PowerYoga": 364,
        "Canoagem": 319,
        "Boliche": 273,
        "Dança de Salão": 273,
        "Tai chi": 273,
        "Caminhada (4 km/h)": 255,
        "Hatha Yoga": 228,
        # Adicione outros exercícios e médias aqui
    }

    return calories_mapping.get(exercise_type, 0)

# Função para calcular as calorias queimadas com base nas calorias por hora e na duração


def calculate_calories_burned(calories_per_hour, duration):
    return round((calories_per_hour * duration) / 60, 2) if duration != 0 else 0


# Rota para a tela de registro de refeições


@app.route("/registro_refeicoes", methods=["GET", "POST"])
def registro_refeicoes():
    username = request.args.get("username")
    user_profile = user_profiles.get(username, {"refeicoes": []})

    if request.method == "POST":
        refeicao = request.form.get("refeicao")
        calorias = int(request.form.get("calorias"))
        tipo_refeicao = request.form.get("tipo_refeicao")

        if "refeicoes" not in user_profile:
            user_profile["refeicoes"] = []

        user_profile["refeicoes"].append({
            "refeicao": refeicao,
            "calorias": calorias,
            "tipo_refeicao": tipo_refeicao
        })

    return render_template("registro_refeicoes.html", username=username, user_profile=user_profile)


# Rota de Cotrole
@app.route('/controle')
def mostrar_controle():
    # Adicione a definição da variável user_profile aqui ou obtenha os dados relevantes de alguma fonte
    # Por exemplo, você pode definir user_profile como um dicionário vazio se não houver dados específicos para essa rota
    user_profile = {}

    return render_template('controle.html', user_profile=user_profile)

# Rota de Feedback

@app.route('/feedback')
def feedback():
    # Lógica para a página de feedback
    return render_template('feedback.html')

if __name__ == "__main__":
    app.run(debug=True)
