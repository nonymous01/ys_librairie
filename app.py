from flask import Flask, redirect,request,render_template, url_for,flash,session,render_template_string
from os  import environ
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///base_data.db'
app.config['SECRET_KEY']='DEDYMAMOUTYOUSSEFDURANT'
db= SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email=db.Column(db.String(50), unique=True, nullable=False)
    tel=db.Column(db.String)
    password= db.Column(db.String(30))

    def __init__(self, name,email,tel,password):
        self.name=name
        self.email=email
        self.tel=tel
        self.password=password 

#cree la BD
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("erreur de la creation de la base de données")

#Accueil Non connecter
@app.route("/")
def indexx():
            return render_template('index.html')


@app.route("/panier")
def panier():
    return render_template('panier.html')



#vers la page de profil
@app.route("/admin")
def admin():
        return render_template("admin.html")

#la liste des commandes
@app.route("/commande")
def commande():
        return render_template("commande.html")

@app.route("/payement")
def payement():
        return render_template("payement.html")



#afficher le form modifier
@app.route("/modif")
def modif():
        return render_template("modifier.html")



#Pour l'inscription
@app.route("/register", methods=['POST','GET'])
def register():
        if request.method=='POST':
            name=request.form['name']
            email=request.form['email']
            tel=request.form['tel']
            password =request.form['password']     
            if len(tel)>=10 and len(password)>=8 :
                try:
                    new_user=User(name,email,password,tel)
                    db.session.add(new_user)
                    db.session.commit()
                    flash(f"Bienvenue!  {name}")
                    return render_template('connexion.html')
                except Exception as e:
                    flash("Erreur Utilisateur existe'")
                    return redirect(url_for('register'))
            else:
               flash("Mot de passe ou nom trop court")
        return render_template("inscription.html")


#Pour la connexion 
@app.route('/login', methods=['GET','POST'])
def login():
    user = User.query.all()
    if request.method =='POST':
        email =request.form['email']
        password= request.form['password']
        #selection d'un utilisateur dans la class User
        user =User.query.filter_by(email=email, password=password).first()
        if user:
            #afficher le nom sur la page d'accueil
            session['user_name']=user.name
            session['user_email']=user.email
            session['user_tel']=user.tel
            return redirect("ajouter")
        elif email =="youssef@gmail.com" and password == "youssef":
            flash("bienvenue ANONYMOUS")
            return redirect('/data')         
        else:
            flash('Identifiants incorrects')
    return render_template('connexion.html')



#afficher la liste des utilisateurs
@app.route('/data', methods = ["GET"])
def data():
    listdata=User.query.all()
    return render_template('datalist.html',listdata=listdata)


# supp les info de la db
@app.route('/users/<int:id>')
def delete_user(id):
    data= User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect("/data")

#ajouter un utilisateur
@app.route("/add_user", methods=['POST','GET'])
def add_user():
        if request.method=='POST':
            name=request.form['name']
            email=request.form['email']
            tel=request.form['tel']
            password =request.form['password']     
            if len(tel)>=10 and len(password)>=8 :
                try:
                    new_user=User(name,email,tel,password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('data'))
                except Exception as e:
                    flash("Erreur Utilisateur existe'")
                    return redirect(url_for('data'))
            else:
               flash("Mot de passe ou nom trop court")
        return render_template("ajouter.html")

#ajouter des articles
class img(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     name=db.Column(db.Text)
     prix=db.Column(db.Text)
     
     def __init__(self,name,prix):
        self.name=name
        self.prix=prix

@app.route('/ajouter', methods =(["GET","POST"]))
def ajouter():
     ajout=img.query.all()
     return render_template('accueil.html',ajout=ajout)

@app.route("/image")
def image():
    return render_template("add_image.html")

    
@app.route('/article', methods = ["POST"])
def article():
        #ajout=img.query.all()
        name = request.form.get("name")
        #image= request.files("file")
        prix = request.form.get("prix")
        db.session.add(img(name=name,prix=prix))
        db.session.commit()
        return redirect("ajouter")
        


from bs4 import BeautifulSoup       
#paiement 
@app.route("/paiement", methods=["GET","POST"])
def paiement():
    if request.method =="POST":
        name_carte = request.form.get('name_carte')
        num_carte = request.form.get('num_carte')
        Expiry = request.form.get('Expiry')
        security = request.form.get('security')
        html = '<div >$232</div>'
        if len(num_carte)==14:
            if len(security)==3:
               soup = BeautifulSoup(html, 'html.parser')
               valeur = soup.div.text.strip('$')
               flash(f"Paiement effectué. Votre compte a été débité de {valeur}$")
               return render_template('payement.html')
            flash ("code de securité incorrect")
            return render_template('payement.html')
        flash ("numero de carte incorrect")
        return render_template('payement.html')
    return render_template('payement.html')
    


# modifier un utilisateur dans la db
@app.route('/update/<int:id>', methods = ["GET","POST"])
def update(id):
    user =User.query.get(id)
    if user:
        if request.method == "POST":
            user.name = request.form.get("name")
            user.email = request.form.get("email")
            user.tel = request.form.get("tel")
            user.password  = request.form.get("password")
            try:
                db.session.commit()
                return redirect('/data')
            except:
                return "Erreur lors de la modification"
    return render_template("modifier.html", user=user)

#afficher le profile
@app.route("/profil/<int:id>", methods = ["GET","POST"])
def profil(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.name = request.form.get("name")
        user.email = request.form.get("email")
        user.tel = request.form.get("tel")
        if user:
            #afficher le nom sur la page d'accueil
            session['user_name']=user.name
            session['user_email']=user.email
            session['user_tel']=user.tel
            return render_template('admin.html',user=user)
        
       


class panier_user(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     name=db.Column(db.Text, nullable=False)
     prix=db.Column(db.Text, nullable=False)
     email=db.Column(db.Text, nullable=False)
     def __init__(self,name,prix,email):
        self.name=name
        self.prix=prix
        self.email=email

@app.route("/show_panier")
def show_panier():
    datas=panier_user.query.all()
    cpt =0
    for _ in datas:
        cpt=cpt+1
    return render_template('panier.html', datas = datas)


@app.route("/accueil")
def connect():
    cpt = show_panier()  # Obtenez la valeur de `cpt`
    return render_template("accueil.html")

@app.route('/paniers', methods =(["GET"]))
def paniers():
     email = session['user_email']
     ajout=panier_user.query.filter_by(email=email).all()
     return redirect("show_panier")

@app.route('/panier_ajoute', methods = ["POST"])
def panier_ajoute():
    if request.method == "POST":
        name = request.form.get('name')
        prix = request.form.get('prix')
        email = session['user_email'] 
        print(name,prix,email)
        db.session.add(panier_user(name=name,prix=prix,email=email))
        db.session.commit()
        return redirect("/ajouter")
    return render_template('panier.html')

# supp les info de la class panier

@app.route('/panier_sup/<int:id>')
def panier_sup(id):
    data = panier_user.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
    return redirect("/paniers") 

@app.route('/logout')
def logout():
    session.clear()  # Efface toutes les données de session
    return redirect(url_for('indexx'))  # Redirige l'utilisateur vers la page d'accueil (ou une autre page appropriée)




if __name__=="__main__":
     app.run(debug=True, port=5000)
    

    
