function compteur=simu_nbr_blocs_attente(nbr_transac_minute,mempool,temps_bloc,taille_transac)

% nbr_transac_minute: maxi=188.7
% mempool: taille de la mempool au départ en kB. 
% temps_bloc: nombre de minutes pour trouver un bloc en moyenne
% taille_transac en kB
    compteur=0;
    if (nbr_transac_minute*taille_transac*temps_bloc<1000)
        while(mempool>=0)
            mempool=mempool+exprnd(temps_bloc*nbr_transac_minute*taille_transac)-1000;
            compteur=compteur+1;
        end
    else        
        'proba que la mempool n arrive jamais a 0 non nulle'
    end
end
