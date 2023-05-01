from gurobipy import Model, GRB



def determiner_pl4_(interface):

    demand_m1 = float(interface.demande_mois_1.toPlainText())
    demand_m2 = float(interface.demande_mois_2.toPlainText())
    demand_m3 = float(interface.demande_mois_3.toPlainText())
    demand_m4 = float(interface.demande_mois_4.toPlainText())
    Di = [demand_m1, demand_m2, demand_m3, demand_m4]
    

    Sal = int(interface.ouvirer_payee_mois.toPlainText())

    Ci = float(interface.cout_matiere_premiere.toPlainText())
    Csi = float(interface.cout_stockage_paire.toPlainText())

    Hsup = float(interface.paye_heure.toPlainText())
    R = float(interface.frais_recrutement_ouvirier.toPlainText())
    L = float(interface.frais_licenciement.toPlainText())
    h = float(interface.chassure_prendre_heures.toPlainText())
    H = float(interface.ouvrier_tavaille_heures.toPlainText())
    Hmax = float(interface.ouvrier_maximum_heures_supplementaire.toPlainText())
    
    paires_stock = float(interface.paires_stock.toPlainText())
    nb_ouvirers = float(interface.nb_ouvirers.toPlainText())

    """   


    Sal = int(interface.ouvirer_payee_mois.toPlainText())
    Csi = int(interface.cout_stockage_paire.toPlainText())
    Ci = int(interface.cout_matiere_premiere.toPlainText())
    
    Hsup = int(interface.paye_heure.toPlainText())
    h = int(interface.chassure_prendre_heures.toPlainText())
    H = int(interface.ouvrier_tavaille_heures.toPlainText())

    R = int(interface.frais_recrutement_ouvirier.toPlainText())
    L = int(interface.frais_licenciement.toPlainText())
    Hmax = int(interface.ouvrier_maximum_heures_supplementaire.toPlainText())
    """

    # Création du modèle
    model = Model("ChausseTous")

    # Variables de décision

    # Variables de décision
    """
    * NHSi : Len nombre d’heures supplémentaires du mois i : (i=1, 2, 3, 4)
    * NCHi : Le nombre de paires de chaussures fabriqués à la fin de chaque mois i.
    * NORi : Le nombre d’ouvriers recrutés au début de chaque mois i.
    * NOLi : Le nombre d’ouvriers licenciés au début de chaque mois i.
    """
    NHS = model.addVars(4, vtype=GRB.INTEGER, name="NHS")
    NCH = model.addVars(4, vtype=GRB.INTEGER, name="NCH")
    NOR = model.addVars(4, vtype=GRB.INTEGER, name="NOR")
    NOL = model.addVars(4, vtype=GRB.INTEGER, name="NOL")

    # Variables auxiliaires
    S = model.addVars(5, vtype=GRB.INTEGER, name="S")
    NO = model.addVars(5, vtype=GRB.INTEGER, name="NO")

    # Fonction objectif
    model.setObjective(sum(Csi * S[i] for i in range(1,5)) + 
                    sum(Sal * NO[i] for i in range(1, 5)) + 
                    sum(Hsup * NHS[i] for i in range(4)) + 
                    sum(R * NOR[i] for i in range(4)) + 
                    sum(L * NOL[i] for i in range(4)) + 
                    sum(Ci * NCH[i] for i in range(4)), GRB.MINIMIZE)
    """
        # Fonction objectif
    model.setObjective(sum(Csi[i] * S[i] for i in range(4)) + 
                    sum(Sal * NO[i] for i in range(1, 5)) + 
                    sum(Hsup * NHS[i] for i in range(4)) + 
                    sum(R * NOR[i] for i in range(4)) + 
                    sum(L * NOL[i] for i in range(4)) + 
                    sum(Ci[i] * NCH[i] for i in range(4)), GRB.MINIMIZE)
    """

    # Contraintes
    model.addConstr(S[0] == paires_stock)
    model.addConstr(NO[0] == nb_ouvirers)
    for i in range(4):
        model.addConstr(NHS[i] <= Hmax * NO[i + 1])
        model.addConstr(S[i] + NCH[i] >= Di[i])
        model.addConstr(NCH[i] <= (1/h) * (H * NO[i + 1] + NHS[i]))
      
        model.addConstr(NO[i + 1] == NO[i] + NOR[i] - NOL[i])
        model.addConstr(S[i + 1] == S[i] + NCH[i] - Di[i])
        ## a corriger 
        
    model.addConstr(S[4] == S[3] + NCH[3] - Di[3])

    for i in range(1, 5):
        model.addConstr(S[i] >= 0)
        model.addConstr(NO[i] >= 0)
        model.addConstr(NOR[i - 1] >= 0)
        model.addConstr(NOL[i - 1] >= 0)
        model.addConstr(NHS[i - 1] >= 0)

    # Résoudre le modèle
    model.optimize()
    stock_final = [0,0,0,0]
    # Afficher les résultats
    print("Résultats :")
    print("------------")
    for i in range(4):
        print(f"Mois {i+1}:")
        print(f"  Demande du mois : {Di[i]}")
        print(f"  Nombre de paires de chaussures fabriquées  : {NCH[i].x}")
        stock_final[i] = S[i].x + NCH[i].x - Di[i]
        print(f"  Nombre de chaussures stockées à la fin du mois  : {stock_final[i]}")

        print(f"  Nombre d'ouvriers recrutés : {NOR[i].x}")
        print(f"  Nombre d'ouvriers licenciés : {NOL[i].x}")
        print(f"  Heures normales : {NCH[i]*h}")
        print(f"  Nombre d’heures supplémentaires  : {NHS[i].x}")
        print(f"  Stock initial au début du mois : {S[i].x}")
        print(f"  Nombre d'ouvriers disponibles  : {NO[i+1].x}")
        print("")

    print(f"Coût total minimum : {model.objVal}")
    interface.fo_s1_pl4.setText(str(round(model.objVal,3)))

    interface.ouvriers_m1.setText(str(round(NO[1].x,3)))
    interface.ouvriers_m2.setText(str(round(NO[2].x,3)))
    interface.ouvriers_m3.setText(str(round(NO[3].x,3)))
    interface.ouvriers_m4.setText(str(round(NO[4].x,3)))
    
    interface.r_mois1.setText(str(round(NOR[0].x,3)))
    interface.r_mois2.setText(str(round(NOR[1].x,3)))
    interface.r_mois3.setText(str(round(NOR[2].x,3)))
    interface.r_mois4.setText(str(round(NOR[3].x,3)))
    
    interface.l_mois1.setText(str(round(NOL[0].x,3)))
    interface.l_mois2.setText(str(round(NOL[1].x,3)))
    interface.l_mois3.setText(str(round(NOL[2].x,3)))
    interface.l_mois4.setText(str(round(NOL[3].x,3)))

    interface.heures_normales_1.setText(str((NCH[i].x*h)))
    interface.heures_normales_2.setText(str((NCH[i].x*h)))
    interface.heures_normales_3.setText(str((NCH[i].x*h)))
    interface.heures_normales_4.setText(str((NCH[i].x*h)))
    
    interface.heures_supp_1.setText(str(round(NHS[0].x,3)))
    interface.heures_supp_2.setText(str(round(NHS[1].x,3)))
    interface.heures_supp_3.setText(str(round(NHS[2].x,3)))
    interface.heures_supp_4.setText(str(round(NHS[3].x,3)))


    interface.p_mois1.setText(str(round(NCH[0].x,3)))
    interface.p_mois2.setText(str(round(NCH[1].x,3)))
    interface.p_mois3.setText(str(round(NCH[2].x,3)))
    interface.p_mois4.setText(str(round(NCH[3].x,3)))
    
    interface.s_mois1.setText(str(round(stock_final[0],3)))
    interface.s_mois2.setText(str(round(stock_final[1],3)))
    interface.s_mois3.setText(str(round(stock_final[2],3)))
    interface.s_mois4.setText(str(round(stock_final[3],3)))

def init_interface_(interface):
    demandes = [3000, 5000, 2000, 1000]

    
    paires_stock = 500
    
    nb_ouvirers = 100
    
    ouvirer_payee_mois = 1500
    ouvrier_tavaille_heures = 160
    
    ouvrier_maximum_heures_supplementaire = 20
    
    paye_heure  = 13
    
    chassure_prendre_heures = 4
    
    cout_matiere_premiere = 15
    frais_recrutement_ouvirier = 1600
    frais_licenciement = 2000
    cout_stockage_paire = 3
    
    interface.demande_mois_1.setText(str(demandes[0]))
    interface.demande_mois_2.setText(str(demandes[1]))
    interface.demande_mois_3.setText(str(demandes[2]))
    interface.demande_mois_4.setText(str(demandes[3]))
    
    interface.paires_stock.setText(str(paires_stock))
    
    interface.nb_ouvirers.setText(str(nb_ouvirers))
    interface.ouvirer_payee_mois.setText(str(ouvirer_payee_mois))

    interface.ouvrier_tavaille_heures.setText(str(ouvrier_tavaille_heures))
    interface.ouvrier_maximum_heures_supplementaire.setText(str(ouvrier_maximum_heures_supplementaire))
    interface.paye_heure.setText(str(paye_heure))
    interface.chassure_prendre_heures.setText(str(chassure_prendre_heures))
    interface.cout_matiere_premiere.setText(str(cout_matiere_premiere))

    interface.frais_recrutement_ouvirier.setText(str(frais_recrutement_ouvirier))
    interface.frais_licenciement.setText(str(frais_licenciement))

    interface.cout_stockage_paire.setText(str(cout_stockage_paire))

