"""
Le code d'origine du fichier javascript traçant les différents segments de la figure

but : transformer ce code en python

v1x = -Math.sqrt(3) * longueur / 2
v1y = longueur / 2;
v2x = 0;
v2y = longueur;
v3x = Math.sqrt(3) * longueur / 2
v3y = longueur / 2;
centrex = Math.sqrt(3) / 2 * longueur * taille + marge
centrey = marge;
 for (j = 0; j < 2 * taille; j++) {
            for (i = 0; i < Math.min(taille + 1, 2 * taille - j); i++) {
                k = 0;
                if ((j > 0) && (i < taille)) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                    ])
                }
                if (i < taille) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                    ])
                }
                if (i > 0) {
                    tabsegment.push([
                        [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                        [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                    ])
                }
            }
        }

partie droite
for (j = 0; j < 2 * taille; j++) {
        for (k = 0; k < Math.min(taille + 1, 2 * taille - j); k++) {

            i = 0;

            if ((j > 0) && (k < taille)) {
                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + i * v1x + j * v2x + (k + 1) * v3x, centrey + i * v1y + j * v2y + (k + 1) * v3y]
                ];
            }
            if ((k < taille) && (k > 0)) {

                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + i * v1x + (j + 1) * v2x + k * v3x, centrey + i * v1y + (j + 1) * v2y + k * v3y]
                ];
            }
            if (k > 0) {

                tabsegment[cpt] = [
                    [centrex + i * v1x + j * v2x + k * v3x, centrey + i * v1y + j * v2y + k * v3y],
                    [centrex + (i + 1) * v1x + j * v2x + k * v3x, centrey + (i + 1) * v1y + j * v2y + k * v3y]
                ];
}
v1x = -longueur
v1y = longueur;
v2x = 0;
v2y = 2*longueur;
v3x = longueur
v3y = longueur;
"""

def make_tab_segments(taille=3):
    """
    retourne la liste de tous les segments traçables avec la syntaxe utilisée pour l'encodage
    des énigmes.
    La liste est dans l'ordre du tracé des segments dans le code JS : ceci est important
    car le programme web se sert de la position dans une chaîne pour connaître le status
    d'une arête
    """
    # Les coordonnées javascript sont avec origine en haut et axe y vers le bas.
    # le codage des coordonnées pour mes fonctions est avec origine au centre et axe y vers le haut
    # cette fonction effectue la transformation js -> python
    def transf_coord(tab):
        for p in tab:
            p[0][1] = 2*taille - p[0][1]
            p[1][1] = 2*taille - p[1][1]

    tabsegment = []

    # tout ce qui suit n'est qu'une reprise du code JS, avec simplifications
    # car des variables sont inutiles (constamment nulles ...), et mes coordonnées
    # sont entières

    # partie gauche
    for j in range(2*taille):
        for i in range(min(taille+1, 2*taille-j)):
            if j>0 and i<taille:
                tabsegment.append([[-i, i + 2*j],
                            [-(i + 1), (i + 1) + 2*j]])
            if i<taille:
                tabsegment.append([[-i,  i  + 2*j],
                            [ -i, i + 2*(j+1)]])
            if i>0:
                tabsegment.append([[-i, i  + 2*j],
                            [-i + 1, i + 2*j + 1]])
    # partie droite sans la ligne verticale x==0
    for j in range(2 * taille):
            for k in range(min(taille + 1, 2 * taille - j)):
                if ((j > 0) and (k < taille)):
                    tabsegment.append([[ -i + k,2*j + k],
                        [(k + 1),  2*j + (k + 1)]])
                if ((k < taille) and (k > 0)):
                    tabsegment.append([[k,  2*j + k],
                        [ k,  2*(j + 1) + k]])
                if (k > 0):
                    tabsegment.append([[ k, 2*j + k],
                        [-1 + k, 1 + 2*j + k]])

    # tabsegment est maintenant une liste de segments, chaque segment est de la
    # forme [A,B], A et B étant des points, donc des listes de la forme [x, y]
    # dans le système de coordonnées JS.

    # on passe en coordonnées Python en modifiant tabsegment
    transf_coord(tabsegment)

    # on va maintenant transformer chaque segment pour passer dans la même syntaxe
    # que celle utilisée pour l'encodage Python des énigmes (X, Y, direction)

    l = [] # la liste résultat qui sera rendue par la fonction
    for cp in tabsegment: # pour chaque segment <-> couple de points
        A, B = cp[0], cp[1]
        if A[0]==B[0]: # segment selon z, l'origine est le point le plus bas
            if A[1]>B[1]:
                l.append(tuple(B + ["z"]))
            else:
                l.append(tuple(A + [ "z"]))

        elif (A[0]-B[0])*(A[1]-B[1]) > 0: # segment selon x, origine la plus à droite
            if A[0]<B[0]:
                l.append(tuple(B + ["x"]))
            else:
                l.append(tuple(A + ["x"]))
        else: # segment selon y, origine la plus à gauche
            if A[0]<B[0]:
                l.append(tuple(A + ["y"]))
            else:
                l.append(tuple(B + ["y"]))
    # C'est fini
    return l


# la chaîne argument de la page web est de la forme suivante (arène de jeu de taille 3):
# "fffssfsffsfsftssfsssfsfffttfsffsssftfsftsffffsfssffsftssfsffftfsffssfsfs33301"
# t -> arête fixée non modifiable  <=> arête de l'énigme toujours affichée dans la page web
# s -> arête de la solution, non affichée (ça serait trop facile !)
# f -> arête ne faisant pas partie de la solution
# les chiffres à la fin ne sont qu'une référence ver le numéro de l'énigme (ne servent à rien ici)

from calisson import doSolve, projection
from gen_calisson import encodage, encodeSolution
import os, webbrowser

# fonction qui transforme une énigme python en une chaîne d'url ayant le bon format
# pour le script JS de la page de mathix.org
# il suffit alors, sous python, d'invoquer qque chose du genre :

# url = make_url(enigme, 5)
# webbrowser.open(url)

# pour avoir la page de résolution de l'énigme qui s'ouvre dans son navigateur
def make_url(enigme, dim):
    """
    enigme : l'énigme à résoudre. Il est souhaitable (nécessaire !) qu'elle ne
    donne qu'une seule solution.
    dim : la taille de la zone de rangement des cubes

    retourne l'url permettant de tenter la résolution sur mathix.org
    """
    tabseg = make_tab_segments(dim)
    lsol = doSolve(enigme, dim)
    jeu = lsol[0]
    encsol = encodeSolution(encodage(jeu))

    for i in range(dim):
        if not jeu[i, 0, 0]:
            X,Y = projection((i, 0, 0))
            encsol.append((X, Y, 'x'))
        if not jeu[0, i, 0]:
            X,Y = projection((0, i, 0))
            encsol.append((X, Y, 'y'))
        if not jeu[0, 0, i]:
            X,Y = projection((0, 0, i))
            encsol.append((X, Y, 'z'))

    # construction du paramètre de l'url
    str = ""
    for seg in tabseg:
        if seg in enigme:
            str += 't'
        elif seg in encsol:
            str += 's'
        else:
            str += 'f'

    # fini ...

    return 'https://mathix.org/calisson/index.html?tab=' + str


# remarque :
# si on tente d'ouvrir une adresse locale du genre :
# command = 'file://' + os.getcwd() + "/calisson_js/calisson.html?tab=" + str
# avec l'instruction suivante :
# webbrowser.open(command)
#
# Sur mon vieux mac (10.13), ça marche pas, le paramètre est effacé pour le
# navigateur par défaut (chrome). (référence au bug connue et référencée sur le web)
# Si je lance avec safari, ça marche :
# webbrowser.get('Safari').open(command)
#
# Par contre, pas de problème pour une adresse web réelle.
# C'est la raison pour laquelle "https://mathix.org/calisson/index.html?tab="
# est utilisée dans la fonction précédente

import re

def make_enigma_from_url(orgurl):
    """
    orgurl : adresse web contenant une énigme proposée sur le site mathix.org
    Retourne une paire (dim, énigme) où dim est la taille du jeu et énigme en encodage Python

    En détails :
    orgurl est de la forme suivante :
    orgurl = "https://mathix.org/calisson/index.html?tab=fffssffffsstft...sffsfsfssffff455"

    Le nombre à la fin de la chaîne est juste une étiquette de numérotation :
    sans intérêt ici, on la retire.

    Ce qui suit alors "tab=" contient l'encodage de l'énigme (et de la solution ...)
    L'énigme correspond aux arêtes fixées par le concepteur d'énigme, marquées par 't'
    La solution prévue est marquée par 's'
    Les arêtes sont citées dans l'ordre des arêtes calculées par la fonction make_tab_segments.
    """

    # calcul de la taille de jeu
    tab_withnum = orgurl.split("=")[1] # on récupère ce qui suit le "="
    tab = re.findall('[tsf]+', tab_withnum)[0] # on vire le nombre à la fin

    # le nombre d'arêtes est de la forme 3n(3n-1). Plutôt que de résoudre cette équa du 2nd degré
    # on boucle pour déterminer la taille
    # (fortement inspiré du code JavaScript qui fait la même chose)
    dim = 1
    while 3* dim * (3 * dim - 1) < len(tab):
        dim +=1

    # maintenant qu'on a la dimension, on fabrique le tableau de segments
    tabseg = make_tab_segments(dim)

    # et l'énigme (on pourrait aussi extraire la solution, mais ce n'est pas le but)
    enigme = []
    for i, c in enumerate(tab):
        if c == "t":
            enigme.append(tabseg[i])

    return dim, enigme


## pour tester
from calisson import test_solver

# une engime de niveau 5, difficile, n'ayant qu'une solution
enigme = [(-2, 0, 'x'), (2, -2, 'x'), (-2, -2, 'y'), (-1, 7, 'y'), (2, -4, 'y'),
(-3,3,'z'),
(-4,-4,'y'),
(-1,-1,'z'),
(0,-6,'x'),
(2,2,'y'),
(3,1,'y'),
(2,4,'z'),
(0,8,'y'),
(3,-1,'y'),
(1,-5,'x'),
(3, 3, 'z'), (-3, 1, 'x'), (0, -4, 'x'), (1, 1, 'x'), (-1, 3, 'z')
]

# lancement du navigateur sur mathix
url = make_url(enigme, 5)
webbrowser.open(url)

# affichage de la resolution auto de l'énigme
test_solver(enigme,5)

## énigme 459 (correcte)
import re

orgurl = "https://mathix.org/calisson/index.html?tab=ffffftsfffffffsssfsffsfffffffffssftffssftftsffffsfftfssffsffsffffffsfsffsffsftfsfssfsfffttftfffffstfssffffsfffffsffsffsffsssftfffsffsffsfsfffffsffsstftffssfsffffffssffffffsstfsfsftsfffstfffsfsffsfffsffsffftfsfssffffsfsfsssfsfsftsfftssfsffsffffffffssftffsfssffftfssffsfffftsffffssfsfftsftfffsffssstsfsffsfsf459"

dim, enigme = make_enigma_from_url(orgurl)
test_solver(enigme, dim)

## grille 455 mathix incorrecte (non entièrement déterminée)
orgurl = "https://mathix.org/calisson/index.html?tab=fffffffssffffffffsstftfftfffffssfsfsfsffssfsfssfsfsssftftsffsffsfffsftffsffsfftfsfssfsfsffsfsfssssfsfffttfstssfsftfsffsssfsftfssssftfsfsssfsfsfsffsftffffffffffffffffffstfffffstssfffsfsfsssfsfsfstfffffffsfssstsffsfffsffffffftffffffffsfffffffsffffffffsffffffsfstfffssfsffffssfffsftfsffsssffstsfsfsftfsfssffff455"

# ce qui donne :
enigme = \
[# contraintes d'origine (à partir de l'url)
 (-2, 8, 'y'),
 (-3, 5, 'z'),
 (-4, 4, 'z'),
 (-2, 2, 'z'),
 (-3, 3, 'x'),
 (-1, 1, 'z'),
 (-4, -2, 'z'),
 (0, -2, 'z'),
 (-1, -1, 'x'),
 (-2, -2, 'x'),
 (-4, -4, 'x'),
 (-2, -4, 'x'),
 (-4, -8, 'z'),
 (-1, -7, 'y'),
 (5, 7, 'x'),
 (2, 6, 'z'),
 (3, 5, 'y'),
 (1, 5, 'x'),
 (1, 1, 'z'),
 (2, -2, 'y'),
 (3, -5, 'y'),
 (2, -8, 'z'),
 (1, -9, 'z')
 # avec les contraintes d'origine, 8 cubes sont indéterminés

 # deux exemples de levée d'indétermination
 # Exemple 1
 ,
 (0,-6,"z"),
 (5,-3,"z"),
 (4,2,"y"),

 # Exemple 2
 # ,
 # (1,-7,"z"),
 # (5,-3,"z"),
 # (4,4,"y")
 #
 ]

test_solver(enigme,6)

