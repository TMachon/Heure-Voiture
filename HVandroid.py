import time
import os
import sl4a

droid = sl4a.droid()

def main() :
    
    fin = False  # Vrai si l'user souhaite quitter

    while not fin :

        contenu = open("HVfile.txt", "r").read()  # Contenu du fichier de stockage
        option = bool(int(contenu[-1]))           # Vrai si on est parti de la maison
        
        if option : ##Si on est parti##
            
            liste = ["Arriver à l'IUT","Annuler le trajet","Afficher les statistiques","Voir l'historique","Quitter"]
			droid.dialogCreatInput("Choisir une option")
			droid.dialogSetItems(liste)
            droid.dialogShow()
			choix = droid.dialogGetResponde().result['item'] + 1

            if choix == 1 : ##"Arriver à l'IUT"##

                # /Calcul du temps de trajet\ #
                depart = str(open("HVfile.txt", "r").read())[-15:-7]  #Heure de départ
                arrivee = str(time.asctime())[11:19]                  #Heure d'arrivée

                nbSecondes = 0 + int(arrivee[6:8])-int(depart[6:8])   #Nombre de secondes = sec. arrivée - sec. départ
                if nbSecondes<0 : #si le résultat est négatif
                    retenueMinute = -1
                    nbSecondes += 60
                else : retenueMinute = 0
                
                nbMinutes = 0 + int(arrivee[3:5])-int(depart[3:5]) + retenueMinute  #Nombre de minutes = min. arrivée - min. départ
                if nbMinutes<0 : #si le résultat est négatif
                    retenueHeure = -1
                    nbMinutes += 60
                else : retenueHeure = 0

                nbHeures = 0 + int(arrivee[:2])-int(depart[:2]) + retenueHeure      #Nombre d'heures = h. arrivée - h. départ
                if nbHeures<0 : annulerTrajet() #si nombre d'heures négatif -> annuler le trajet
                
                tempsTrajet = str(nbHeures).zfill(2)+ ":" +str(nbMinutes).zfill(2)+ ":" +str(nbSecondes).zfill(2)
                # \Fin calcul du temps de trajet/ #
                
                open("HVfile.txt", "w").write(contenu[:-1]+time.asctime()+"|Trajet:"+tempsTrajet+"\n0")

            elif choix == 2 : ##"Annuler le trajet"##
                annulerTrajet(contenu)

            elif choix == 3 : ##"Afficher les statistiques"##
                droid.dialogCreateAlert("Statistiques",statistiques(contenu))
				droid.dialogShow()

            elif choix == 4 : ##"Voir l'historique"##
                droid.dialogCreateAlert("Historique",historique(option))
				droid.dialogShow()

            else : fin = True ##"Quitter"##
                
        else : ##Si on est pas encore parti##
            
            liste = ["Afficher l'heure de départ","Partir de la maison","Afficher les statistiques","Voir l'historique","Quitter"]
            droid.dialogCreatInput("Choisir une option")
			droid.dialogSetItems(liste)
            droid.dialogShow()
			choix = droid.dialogGetResponde().result['item']
			
			if choix == 0 : ##"Afficher l'heure de départ"##
				droid.makeToast(contenu[-26:-2])
                
            elif choix == 1 : ##"Partir de la maison"##
                open("HVfile.txt", "w").write(contenu[:-1]+time.asctime()+"|1")
                
            elif choix == 2 : ##"Afficher les statistiques"##
                droid.dialogCreateAlert("Statistiques",statistiques(contenu))
				droid.dialogShow()

            elif choix == 3 : ##"Voir l'historique"##
                droid.dialogCreateAlert("Historique",historique(option))
				droid.dialogShow()

            else : fin = True ##"Quitter"##

def annulerTrajet(contenu) :
    open("HVfile.txt", "w").write(contenu[:-26]+"0")

def statistiques(chaine) -> str :
    liste = chaine.split('\n')
    moyenneDepart = [0,0,0]
    moyenneArrivee = [0,0,0]
    moyenneTrajet = [0,0,0]
    heureDepartMin = [int(liste[0][11:13]), int(liste[0][14:16]), int(liste[0][17:19])]
    heureDepartMax = [int(liste[0][11:13]), int(liste[0][14:16]), int(liste[0][17:19])]
    heureArriveeMin = [int(liste[0][36:38]), int(liste[0][39:41]), int(liste[0][42:44])]
    heureArriveeMax = [int(liste[0][36:38]), int(liste[0][39:41]), int(liste[0][42:44])]
                      
    for i in range(len(liste)-1) :
        moyenneDepart[0] += int(liste[i][11:13])
        moyenneDepart[1] += int(liste[i][14:16])
        moyenneDepart[2] += int(liste[i][17:19])
        moyenneArrivee[0] += int(liste[i][36:38])
        moyenneArrivee[1] += int(liste[i][39:41])
        moyenneArrivee[2] += int(liste[i][42:44])
        moyenneTrajet[0] += int(liste[i][57:59])
        moyenneTrajet[1] += int(liste[i][60:62])
        moyenneTrajet[2] += int(liste[i][63:65])

        if int(liste[i][11:13])<heureDepartMin[0] :
            heureDepartMin = [int(liste[i][11:13]), int(liste[i][14:16]), int(liste[i][17:19])]
        elif int(liste[i][11:13])==heureDepartMin[0] and int(liste[i][14:16])<heureDepartMin[1] :
            heureDepartMin = [int(liste[i][11:13]), int(liste[i][14:16]), int(liste[i][17:19])]
                              
        if int(liste[i][11:13])>heureDepartMax[0] :
            heureDepartMax = [int(liste[i][11:13]), int(liste[i][14:16]), int(liste[i][17:19])]
        elif int(liste[i][11:13])==heureDepartMax[0] and int(liste[i][14:16])>heureDepartMax[1] :
            heureDepartMax = [int(liste[i][11:13]), int(liste[i][14:16]), int(liste[i][17:19])]

        if int(liste[i][11:13])<heureArriveeMin[0] :
            heureArriveeMin = [int(liste[i][36:38]), int(liste[i][39:41]), int(liste[i][42:44])]
        elif int(liste[i][11:13])==heureArriveeMin[0] and int(liste[i][14:16])<heureArriveeMin[1] :
            heureArriveeMin = [int(liste[i][36:38]), int(liste[i][39:41]), int(liste[i][42:44])]
                              
        if int(liste[i][11:13])>heureArriveeMax[0] :
            heureArriveeMax = [int(liste[i][36:38]), int(liste[i][39:41]), int(liste[i][42:44])]
        elif int(liste[i][11:13])==heureArriveeMax[0] and int(liste[i][14:16])>heureArriveeMax[1] :
            heureArriveeMax = [int(liste[i][36:38]), int(liste[i][39:41]), int(liste[i][42:44])]
                      
    for i in range(3) :
        moyenneDepart[i] = int(moyenneDepart[i]/(len(liste)-1))
        moyenneArrivee[i] = int(moyenneArrivee[i]/(len(liste)-1))
        moyenneTrajet[i] = int(moyenneTrajet[i]/(len(liste)-1))

    affichage = "Heure moyenne de départ : "+str(moyenneDepart[0]).zfill(2)+":"+str(moyenneDepart[1]).zfill(2)+":"+str(moyenneDepart[2]).zfill(2)+"\n"
    affichage += "Heure moyenne d'arrivée : "+str(moyenneArrivee[0]).zfill(2)+":"+str(moyenneArrivee[1]).zfill(2)+":"+str(moyenneArrivee[2]).zfill(2)+"\n"
    affichage += "Temps moyen de trajet : "+str(moyenneTrajet[0]).zfill(2)+":"+str(moyenneTrajet[1]).zfill(2)+":"+str(moyenneTrajet[2]).zfill(2)+"\n"
    affichage += "Heure de départ minimale : "+str(heureDepartMin[0]).zfill(2)+":"+str(heureDepartMin[1]).zfill(2)+":"+str(heureDepartMin[2]).zfill(2)+"\n"
    affichage += "Heure de départ maxiamle : "+str(heureDepartMax[0]).zfill(2)+":"+str(heureDepartMax[1]).zfill(2)+":"+str(heureDepartMax[2]).zfill(2)+"\n"
    affichage += "Heure minimale d'arrivée : "+str(heureArriveeMin[0]).zfill(2)+":"+str(heureArriveeMin[1]).zfill(2)+":"+str(heureArriveeMin[2]).zfill(2)+"\n"
    affichage += "Heure maximale d'arrivée : "+str(heureArriveeMax[0]).zfill(2)+":"+str(heureArriveeMax[1]).zfill(2)+":"+str(heureArriveeMax[2]).zfill(2)+"\n"

    return affichage
                           
def historique(parti) :

    histo = open("HVfile.txt", "r").read()
    if parti : return histo[:-1]+" ... En route ..."
    else : return histo[:-1]
    
main() 
