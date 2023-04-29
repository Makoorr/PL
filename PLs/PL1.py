import gurobipy as gp

class PL1:
    def __init__(self):
        # Parametres du probleme
        Rendement = [75,60,55,50,60]
        Prix_vente = [60,50,66,110,60]
        Main_doeuvre = [2,1,2,3,2]
        Temps_machine = [30,24,20,28,25]
        Eau = [3000,2000,2500,3800,3200]
        Salaire_annuel = [500,500,600,700,550]
        Frais_gestion = [250,180,190,310,320]

        # Valeurs des contraintes
        main_doeuvre = 3000
        eau_dirrigation = 25000000
        heure_machine = 24000

        model = gp.Model("PL1")

        x = model.addVars(range(5) , name="x")

        # Fonction d'objective
        model.setObjective(gp.quicksum( x[i] * (
                                ( Rendement[i]*Prix_vente[i] )
                                - ( Main_doeuvre[i]*Salaire_annuel[i] )
                                - ( Temps_machine[i]*30 )
                                - ( Eau[i]*0.1 )
                            ) - Frais_gestion[i]
                            for i in range(5)),gp.GRB.MAXIMIZE)

        # Contraintes
        model.addConstr(gp.quicksum( (Main_doeuvre[i]*x[i]) for i in range(5)) <= main_doeuvre)
        model.addConstr(gp.quicksum( (Temps_machine[i]*x[i]) for i in range(5)) <= heure_machine)
        model.addConstr(gp.quicksum( (Eau[i]*x[i]) for i in range(5)) <= eau_dirrigation)
        for i in range(5):
            model.addConstr(x[i] >= 0)
        model.addConstr(gp.quicksum( x[i] for i in range(5)) <= 1000)

        # Resolution
        model.optimize()

        # Affichage des resultats
        for v in model.getVars():
            print('%s %g' % (v.varName, v.x))