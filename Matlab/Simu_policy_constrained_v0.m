% Simulate investment barrier with finite horizon of 2 years
function [Pmesh, policy, cutoff] = Simu_policy_constrained(param,alpha,sigma2,r)


%% SECTION 1: Environment / Initialization / Parameters


%----% Flags %------------------------------------------------------------%
%

version         = 0;
revision        = 0;
date            = 'July, 2019';

kpic            = 1;
flag_pic        = 1;                                                        % 1 = debug mode 
flag_approx     = 1;                                                        % 1 = polynomial approximation of barrier (needs curve fitting toolbox)
flag_check      = 0;                                                        % 1 = check that the barrier is accurate 

% % Script header
% disp(' ');
% disp('Bitcoin Barrier constrained');
% disp(' ');
% tag          = sprintf('Date...................: %s', date); disp(tag);
% tag          = sprintf('Version................: %2.1f.%1.0f', version, revision); disp(tag);
% disp(' ');

%-----% Main parameters %-------------------------------------------------%

% Parameters

% Period length in years

length_time          = param(1);

% NOtice: Quarters are time units!
a               = param(2);

% Investment Costs

eta             = param(3);
scale           = param(4);

I               = 1;
I_T             = I;


% Parameters of Brownian

%Quarterly estimates
alpha           = alpha;                                                       % Trend brownian

mu              = alpha+a;

sigma           = sqrt(sigma2);


r               = r;

%----------------------% Grid parameters%-----------------------------%

% Time horizon
horizon         = 2;                                                       % Time horizon (5 quarters)        

% Discretization of time 
tmin                        = 0;
tmax                        = horizon;
number_observation_year     = 200;
N                           = tmax*number_observation_year;                 % size of the grid (time)
deltat                      = (tmax-tmin)/N;                              % step (time)
Tmesh_n                     = tmax:-deltat:tmin;                            % Descending order (CAUTION!)


%-----% Create a structure for the parameters %---------------------------%

par.r           = r;
par.I           = I;
par.mu          = mu;
par.sigma       = sigma;


%% SECTION 2: Build Time Dependent Barrier 

disp(' ')
        
%---------%Store variables%----------------------------------------------%
 
Barrier_buffer       = zeros(N+1,1);
Barrier_norm_buffer  = zeros(N+1,1);
if flag_approx==1
Barrier_apx_buffer   = zeros(N+1,1);
end

% The model is solved backward. 

% Step 1: Evaluate R (reservation productivity at the final date t=T in the last iteration period)

%Evaluate the caracteristic equation of the Cauchy-Euler equation
coef            = [sigma^2/2 (mu-sigma^2/2) -r-a];
beta            = roots(coef);
beta1           = max(beta);                                               % Positive root
beta2           = min(beta);                                               % Negative root (unused)


P_bar             = (beta1/(beta1-1))*(r-alpha);

V_fun           = @(P) P./(r-alpha)-(1/(beta1-1))*((P)/((beta1/(beta1-1))*(r-alpha)))^beta1;

Sol_fun         = @(P) (P<P_bar)*(V_fun (P))+...  % Merge 2 solutions
                        (P>=P_bar)*1;

% Generate grids

% Discretization of productivity (log) (index i)
Pmin            = 0;
% Productivity grid including PstarT
Pmax                        = P_bar*5;
deltaP                      = (Pmax-Pmin)/250;
Pmesh                       = Pmin:deltaP:Pmax;
M                           = length(Pmesh)-1; 

Solution_mesh_buffer    = zeros(N+1,M+1);    
Investment_mesh_buffer  = zeros(N+1,M+1);  

% Time vector
Tmesh                       = tmax:-deltat:tmin;                            % Descending order (CAUTION!)

% Step 2: Evaluate R(t) (Time moving Barrier)
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Set: Buffer for time and productivity %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Set: buffers for V(i,j), productivity, time
Solution_mesh               = Solution_mesh_buffer;
Investment_mesh             = Investment_mesh_buffer;  
Solution_mesh(:)            = NaN;                                          % for test purpose only! 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Set: Terminal and boundary conditions %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Terminal condition at t=T
Solution_mesh(1,:) = Pmesh/r;
for i = 1:length(Pmesh)
    
        P                       = Pmesh(i); 
        SolT                    = Sol_fun(P);   
        Solution_mesh(1,i)      = SolT;
    
end

% Boundary conditions at P=Pmin and P=Pmax (loop over t (time))
for j = 1:length(Tmesh)
    Solution_mesh(j,1)      = 0;          % BC at P = Pmin ---> S(Pmin) = 0
end

Solution_mesh(1:2,M+1)    = Sol_fun(Pmax);          % BC at P = Pmax and T=Tmax = 0 
    

%omega                       = 1.2;                                         % Relaxation parameter (1 = Gauss-Seidel)
tolerance                   = 1e-3;

% loop over time (except for the terminal date that is already known). Last
% iteration will fill the last row of the matrix.

max_iter                    = 200;
check_iter                  = zeros(N,1);

for j = 1:N
j

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Build: Generating functions and tridiagonal matrix %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% generating function for the linear system (in state space )
% fun_a               = @(i) 0.5*deltat*((alpha+a+Investment_mesh(i))*i-sigma^2*i^2);                   % coef
% fun_b               = @(i) 1+Investment_mesh(i)*deltat+(sigma^2*i^2+(r+a))*deltat;                % coef
% fun_c               = @(i) -0.5*(sigma^2*i^2+(alpha+a+Investment_mesh(i))*i)*deltat;                  % coef
% fun_d               = @(i) (i*deltaP+eta*Investment_mesh(i)^(1+eta))*deltat;                       

% generating function for the linear system (in state space )
% Do not correct for approximation of investment policy!
fun_a               = @(i) 0.5*((alpha+a-(i>0)*Investment_mesh(j,max(1,i)))*i-sigma^2*i^2)*deltat;                   % coef
fun_b               = @(i) 1+(sigma^2*i^2+(r+a))*deltat;                % coef
fun_c               = @(i) -0.5*(sigma^2*i^2+(alpha+a-(i>0)*Investment_mesh(j,max(1,i)))*i)*deltat;                  % coef
fun_d               = @(i) (i*deltaP+(i>0)*eta*Investment_mesh(j,max(1,i))^(1+eta))*deltat;                       

% fun_a               = @(i) 0.5*deltat*((alpha+a)*i-sigma^2*i^2);                   % coef
% fun_b               = @(i) 1+(sigma^2*i^2+(r+a))*deltat;                % coef
% fun_c               = @(i) -0.5*(sigma^2*i^2+(alpha+a)*i)*deltat;                  % coef
% fun_d               = @(i) (i*deltaP)*deltat;                          % constant (CAUTION! fun_d is time dependent if flag_epl == 1)

% Tridiagonal matrix
Acoeffs             = zeros(M+1,1);
Bcoeffs             = zeros(M+1,1);
Ccoeffs             = zeros(M+1,1);
Dconsts             = zeros(M+1,1);

for i = 1:M+1
   Acoeffs(i)           = fun_a(i-1);
   Bcoeffs(i)           = fun_b(i-1);
   Ccoeffs(i)           = fun_c(i-1);
   Dconsts(i)           = fun_d(i-1);
end

% Tri is (M-1)*(M-1) matrix
L                   = diag(Acoeffs(3:M),-1);                                % Lower part of the Tridiagonal matrix
D                   = diag(Bcoeffs(2:M));                                   % Diagonal part
U                   = diag(Ccoeffs(2:M-1),+1);                              % Upper part

Tri                 = L+D+U;
TT                  = D\(L+U);                                              % D^-1*(L+U)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Gauss-Seidel/Successive Over Relaxation (SOR) method %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Calculate: optimal relaxation parameter
% use theorem 7.26 in Burden and Faires (2011)
spectral_norm               = max(sqrt(eig(TT'*TT)));
t1                          = 2;
t2                          = 1+sqrt(1-spectral_norm^2);
omega                       = t1/t2;


    % Set RHS (incl. constants terms)
    vec_consts              = zeros(M-1,1);
    vec_consts(1,1)         = fun_a(0)*Solution_mesh(j+1,1)-Dconsts(2);
%    vec_consts(1,1)         = fun_a(0)*Solution_mesh(j+1,1);
    vec_consts(M-1,1)       = fun_c(M)*Solution_mesh(j+1,M+1)-Dconsts(M);
%    vec_consts(M-1,1)       = fun_c(M)*Solution_mesh(j+1,M+1);
   vec_consts(2:M-2,1)     = -Dconsts(3:M-1);
   
    RHS                     = Solution_mesh(j,2:M)'-vec_consts;
    
    % Solving Ax=b iteratively using SOR method
    A                       = Tri;
    b                       = RHS;
   
    x                       = Solution_mesh(j,2:M)';
    %x0                      = zeros(size(x));
    x0                      = x;
    n_iter                  = 0;                                            % Reset n_iter
    error                   = 1;
    
    n                       = length(b);
    while (error > tolerance)&&(n_iter < max_iter)
       n_iter                   = n_iter+1; 
       
       for i = 1:n
          x(i)      = b(i)-A(i,1:i-1)*x(1:i-1)-A(i,i+1:n)*x0(i+1:n);
          x(i)      = x(i)/A(i,i);
          x(i)      = omega*x(i)+(1-omega)*x0(i);         % Check for Barrier
%          x(i)      = min(omega*x(i)+(1-omega)*x0(i),I_T);
 
       end
       error    = norm(x-x0);
       x0       = x;
       
    end
    check_iter(j)                   = n_iter; 
    Solution_mesh(j+1,(2:end-1))  = x;
    
    Solution_mesh(j+1, end)       = interp1(Pmesh(1:end-1),Solution_mesh(j+1,1:end-1),Pmesh(end),'linear','extrap');
    if j<N
    Solution_mesh(j+2, end)       = interp1(Pmesh(1:end-1),Solution_mesh(j+1,1:end-1),Pmesh(end),'linear','extrap');
    end
    Investment_mesh(j+1, :)       = (max(0,Solution_mesh(j+1,:)-1)/((1+eta)*scale)).^(1/eta);
    
end

policy      = Investment_mesh(end,:);
cutoff     = Pmesh(find(Solution_mesh(end,:)>1,1));

end

