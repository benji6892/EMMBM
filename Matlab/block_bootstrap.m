
donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);

%************************************************************************
%                          premiere periode
%************************************************************************

rng(1)

B = 100;

d=812; 
f=1483; 
true_halving=1419;
a=0.003233;
I=5593929;
alpha=0.0065322; 
sigma2=0.0053494; 
precision=5;
r=0.1/365;

debuts=[1, 122 ,278 ,418]; 
halving_bloc = 4; 
halving_day_in_bloc = true_halving - d - debuts(halving_bloc) + 1;

dR = exp(diff(log(R(d:f))));
dQ = exp(diff(log(Q(d:f))));
fins = horzcat(debuts(2:end)-1, length(dR));
nb_blocs = length(debuts);
taille_blocs = fins - debuts + 1;
% needed to find the date of hlaving in the bootstrapped series


v_a = zeros(1, B);
v_I = zeros(1, B);

for b = 1:B
    b
    
    % a valid sample must contain once and only once the block 5 (only one halving).
    sample = datasample(1:nb_blocs,nb_blocs);
    while length(find(sample==halving_bloc)) ~= 1
        sample = datasample(1:nb_blocs,nb_blocs);
    end

    h = d-1;
    s = 1;
    while sample(s) ~= halving_bloc
        h = h + taille_blocs(sample(s));
        s = s + 1;
    end
    h = h + halving_day_in_bloc; % halving day in bootstrap serie.
    
    dRb = [];
    dQb = [];
    for s = 1:nb_blocs
        dRb = vertcat(dRb, dR(debuts(sample(s)): fins(sample(s))));
        dQb = vertcat(dQb, dQ(debuts(sample(s)): fins(sample(s))));
    end
    Rb = zeros(length(dRb) + 1, 1);
    Qb = zeros(length(dQb) + 1, 1);
    Rb(1) = R(d);
    Qb(1) = Q(d);
    for t = 2:length(Rb)
        Rb(t) = Rb(t-1) * dRb(t-1);
        Qb(t) = Qb(t-1) * dQb(t-1);
    end
    Rbtot = vertcat(R(1:(d-1)), Rb);
    Qbtot = vertcat(Q(1:(d-1)), Qb);

    param=estimation_parametres_hf([a,I],Rbtot,Qbtot,d,d+length(Rb)-1,h,alpha,sigma2,r,precision);
    v_a(b) = param(1);
    v_I(b) = param(2);
end

std_a = 365*(sqrt(mean(v_a.^2)-mean(v_a)^2))
std_I = sqrt(mean(v_I.^2)-mean(v_I)^2)

fileID = fopen('bootstrap1.txt','w');
fprintf(fileID,'%e %e\n',std_a,std_I)



% %************************************************************************
% %                          deuxieme periode
% %************************************************************************
% 
% rng(1)
% 
% B = 100;
% 
% d=2095; 
% f=3003; 
% true_halving=2738;
% a=0.0023;
% I=1655;
% alpha=0.00125612; 
% sigma2=0.0014915; 
% precision=5;
% r=0.1/365;
% 
% debuts = [1 ,90, 269, 376, 476, 821]; 
% halving_bloc = 5; 
% halving_day_in_bloc = true_halving - d - debuts(halving_bloc) + 1;
% 
% dR = exp(diff(log(R(d:f))));
% dQ = exp(diff(log(Q(d:f))));
% fins = horzcat(debuts(2:end)-1, length(dR));
% nb_blocs = length(debuts);
% taille_blocs = fins - debuts + 1;
% % needed to find the date of hlaving in the bootstrapped series
% 
% 
% v_a = zeros(1, B);
% v_I = zeros(1, B);
% 
% for b = 1:B
%     b
%     
%     % a valid sample must contain once and only once the block 5 (only one halving).
%     sample = datasample(1:nb_blocs,nb_blocs);
%     while length(find(sample==halving_bloc)) ~= 1
%         sample = datasample(1:nb_blocs,nb_blocs);
%     end
% 
%     h = d-1;
%     s = 1;
%     while sample(s) ~= halving_bloc
%         h = h + taille_blocs(sample(s));
%         s = s + 1;
%     end
%     h = h + halving_day_in_bloc; % halving day in bootstrap serie.
%     
%     dRb = [];
%     dQb = [];
%     for s = 1:nb_blocs
%         dRb = vertcat(dRb, dR(debuts(sample(s)): fins(sample(s))));
%         dQb = vertcat(dQb, dQ(debuts(sample(s)): fins(sample(s))));
%     end
%     Rb = zeros(length(dRb) + 1, 1);
%     Qb = zeros(length(dQb) + 1, 1);
%     Rb(1) = R(d);
%     Qb(1) = Q(d);
%     for t = 2:length(Rb)
%         Rb(t) = Rb(t-1) * dRb(t-1);
%         Qb(t) = Qb(t-1) * dQb(t-1);
%     end
%     Rbtot = vertcat(R(1:(d-1)), Rb);
%     Qbtot = vertcat(Q(1:(d-1)), Qb);
% 
%     param=estimation_parametres_hf([a,I],Rbtot,Qbtot,d,d+length(Rb)-1,h,alpha,sigma2,r,precision);
%     v_a(b) = param(1);
%     v_I(b) = param(2);
% end
% 
% std_a = 365*(sqrt(mean(v_a.^2)-mean(v_a)^2));
% std_I = sqrt(mean(v_I.^2)-mean(v_I)^2);
% 
% fileID = fopen('bootstrap2.txt','w');
% fprintf(fileID,'%e %e\n',std_a,std_I)
