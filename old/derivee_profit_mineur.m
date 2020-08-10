function d=derivee_profit_mineur(St0,Ht0,G,C,E,P,a)
    eps=0.0000001;
    d=(1/eps)*(profit_mineur2(St0+eps,Ht0,G,C,E,P,a)-...
        profit_mineur2(St0,Ht0,G,C,E,P,a));
end