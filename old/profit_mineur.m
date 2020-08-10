function profit=profit_mineur(St0,Ht0,G,C,E,P,a)
    t=0;
    profit=-P;
    gain=G*Ht0/St0-C*E
    while(gain>=0)
        t=t+1
        profit=profit+gain;
        gain=G*Ht0/((a^t)*St0)-C*E
    end
end

% 
% function profit=profit_mineur(St0,Ht0,G,C,E,P,a)
%     t=0;
%     profit=-P;
%     gain=G*Ht0/St0-C*E;
%     while(gain>=0)
%         t=t+1
%         profit=profit+gain;
%         gain=G*Ht0/((a^t)*St0)-C*E;
%     end
% end