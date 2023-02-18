# Alpha-Zero

EXTRAIT DU RAPPORT

Comment utiliser notre code :

Si vous souhaitez jouer contre notre agent ou lancer l’apprentissage de ce dernier, voici les étapes à suivre :

1 - Téléchargez notre code via notre github : https://github.com/MartialLig/Alpha-Zero  
2 - Décompressez le réseau de neurones. Nous avons compressé le fichier pour pouvoir l’upload sur Github.  
3 - Une fois que vous avez décompressé le réseau de neurones, vous avez deux options :  
 A) Si vous voulez entraîner à nouveau l'agent, décommentez la ligne 82 pour relancer l’entraînement dès le début.  
 B) Si vous voulez jouer contre notre agent, décommentez la ligne 85. Vous avez trois options pour déterminer l'adversaire de l'agent :  
 i. En mettant 1 en argument de launch_a_game_to_play(1) : vous pouvez jouer en tant qu'humain et entrer les coordonnées de votre coup.  
 ii. En mettant 2 en argument de launch_a_game_to_play(2) : notre agent affrontera l'agent greedy.  
 iii. En mettant 3 en argument de launch_a_game_to_play(3) : notre agent affrontera un joueur jouant de manière aléatoire.
