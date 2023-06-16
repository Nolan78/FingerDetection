# Detection image de chiffre manuscrit

Executé le init.py au clonage du repo

Le dataset <https://www.kaggle.com/datasets/scolianni/mnistasjpg/discussion>
archive.zip > trainingSet > trainingSet

<table>
    <thead>
        <tr>
            <th colspan="2">Truc à faire</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Refaire l'ihm</td>
            <td>Nolan</td>
            <td>En cours</td>
        </tr>
        <tr>
            <td>Sauvegarder les tableau numpy en fichier cache pour faire l'entrainement plus vite une fois tout chargé</td>
            <td>Clément</td>
            <td>Fait</td>
        </tr>
        <tr>
            <td>Decaler les image a gauche a droite en haut en bas</td>
            <td>Clément</td>
            <td>Fait</td>
        </tr>
        <tr>
            <td>Re entrainé ensuite</td>
            <td>Clément</td>
            <td>Fait</td>
        </tr>
        <tr>
            <td>Rajouter la fonction audio</td>
            <td>Léo</td>
            <td>En cours</td>
        </tr>
        <tr>
            <td>Rajouter la conversion en image noir et blanc automatique pour gérer un mode daltonien</td>
            <td>Léo</td>
            <td>Fait</td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan="5">Statistique</th>
        </tr>
        <tr>
            <th>Source</th>
            <th>Accuracy 20 epochs</th>
            <th>Image 20 epochs</th>
            <th>Accuracy 30 epochs</th>
            <th>Image 30 epochs</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Set de base: 41 979 images</td>
            <td>99.22 %</td>
            <td><img src="stat/model_loss_accuracy_base_20.png"></th>
            <td>99.09 %</td>
            <td><img src="stat/model_loss_accuracy_base_30.png"></th>
        </tr>
        <tr>
            <td>Image decalle: 209 895 images</td>
            <td>99.77 %</td>
            <td><img src="stat/model_loss_accuracy_decalle_20.png"></th>
            <td>99.85 %</td>
            <td><img src="stat/model_loss_accuracy_decalle_30.png"></th>
        </tr>
        <tr>
            <td>Image decalle PLUS: 545 727 images</td>
            <td>99.89 %</td>
            <td><img src="stat/model_loss_accuracy_decalle_plus_20.png"></th>
            <td>99.94 %</td>
            <td><img src="stat/model_loss_accuracy_decalle_plus_30.png"></th>
        </tr>
    </tbody>
</table>
