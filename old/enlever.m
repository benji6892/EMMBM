function d=enlever(donnees,a_enlever)
    N=length(a_enlever);
    if (size(donnees,1)==N)
        d=zeros(N-sum(a_enlever),size(donnees,2));
        indice=1;
        for i=1:N
            if (a_enlever(i)==0)
                d(indice,:)=donnees(i,:);
                indice=indice+1;
            end
        end       
    else
        'les donnees n ont pas la meme taille que le vecteur de selectioin'
        d=donnees;
    end
end