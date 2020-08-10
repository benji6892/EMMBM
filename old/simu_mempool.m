taille_transac=0.53; %kB
nbr_transac_minute=188; %maxi=188.7
t=1000/(taille_transac*nbr_transac_minute); %temps nécessaire pour atteindre 1MB
temps_bloc=10; %nombre de minutes pour trouver un bloc

unite=100;
tpstotal=1200;
longueur=unite*tpstotal;
mempool=nbr_transac_minute*((1/unite):(1/unite):tpstotal)*taille_transac;
curseur=0;
while(curseur<tpstotal)
    curseur=round(exprnd(temps_bloc),2)+curseur;
    if (curseur<tpstotal)
       indice=round(unite*curseur);
       taille_bloc=min(1000,mempool(indice));
       mempool(indice:longueur)=mempool(indice:longueur)-taille_bloc; 
    end
end

plot(1:longueur,mempool);

%.......................................................................
taille_transac=0.53; %kB
nbr_transac_minute=120; %maxi=188.7
temps_bloc=10; %nombre de minutes pour trouver un bloc
mempool=0;
tic
nbr_simu=10000;
somme=0;
donnees=zeros(nbr_simu,1);
for i=1:nbr_simu
    resultat=simu_nbr_blocs_attente(nbr_transac_minute,mempool,...
        temps_bloc,taille_transac);
    donnees(i)=resultat;
    somme=somme+resultat*(resultat+1)/2;
end
toc

somme/sum(donnees)

taille_transac=0.53; %kB
temps_bloc=10; %nombre de minutes pour trouver un bloc
mempool=0;
nbr_simu=10000;
plage=1:1:188;
L=length(plage);
temps_attente=zeros(L,1);
for l=1:L
    nbr_transac_minute=l;
    if mod(l,10)==0
    l
    end
    somme=0;
    donnees=zeros(nbr_simu,1);
    for i=1:nbr_simu
        resultat=simu_nbr_blocs_attente(nbr_transac_minute,mempool,...
            temps_bloc,taille_transac);
        donnees(i)=resultat;
        somme=somme+resultat*(resultat+1)/2;
    end
    temps_attente(l)=somme/sum(donnees);
end
plage2=plage(1:170);
temps_attente2=temps_attente(1:170);
plot(plage2,temps_attente2,plage2,13000./(188.7-plage2).^2)

% histo=zeros(max(donnees),1);
% for i=1:nbr_simu
%     histo(donnees(i))=histo(donnees(i))+1;
% end
% 
% plot(1:length(histo),histo)


