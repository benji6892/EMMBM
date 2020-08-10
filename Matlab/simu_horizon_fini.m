function [Bt,P_star_T]=simu_horizon_fini(a,r,I,alpha,sigma2,horizon,precision)

    mu              = alpha+a;
    sigma           = sqrt(sigma2);
    
    %Evaluate the caracteristic equation of the Cauchy-Euler equation

    coef            = [sigma^2/2 (mu-sigma^2/2) -r-a];
    beta            = roots(coef);
    beta1           = max(beta);                                               % Positive root

    % Investment Costs
    
    I_T             = I*exp(-a*horizon); % temps entre le debut de la periode d'etude et le halving

    % Division Ratio at date T

    Ratio           = 1/2;

    %----------------------% Grid parameters%-----------------------------%
    

    % Discretization of time 
    tmin                        = 0;
    tmax                        = horizon;
    N                           = tmax;                 % size of the grid (time)
    deltat                      = (tmax-tmin)/N;                              % step (time)
    Tmesh_n                     = tmax:-deltat:tmin;                            % Descending order (CAUTION!)

    % Number of periods with division

    N_T             = 1;

    % Generate cost vector

    I_vec           = exp(a.*Tmesh_n);

    %-----% Create a structure for the parameters %---------------------------%

    par.r           = r;
    par.I           = I;
    par.mu          = mu;
    par.sigma       = sigma;


    %% SECTION 2: Build Time Dependent Barrier 

    t=N_T;


    %---------%Store variables%----------------------------------------------%

    
    % Generate cost vector

    I_mesh  = I_vec*I_T*(exp(a.*horizon*(N_T-t)));

    % The model is solved backward. 

    % Step 1: Evaluate R (reservation productivity at the final date t=T in the last iteration period)
    %

    % V_fun           = @(P) P*Ratio/(r-mu);    % Value of computing power at date T
    %                                           % Notice that it takes into account
    %                                           % division by Ratio!
    %                                          
    % V_star_T        = (beta1/(beta1-1))*I;   % Value at which option is exercised
    % P_star_T        = V_star_T.*(r-mu)/Ratio;  % Barrier at date T
    % 
    % Const           = (V_star_T-I)/V_star_T.^beta1; % Constant in real options
    % 
    % F_option_fun    = @(P) Const*((P*Ratio)/(r-mu)).^beta1;    % Value of option below barrier
    % 
    % Sol_fun         = @(P) (P<=P_star_T)*(V_fun (P) - F_option_fun(P))+...  % Merge 2 solutions
    %                         (P>P_star_T)*I;

    P_star_T        = (beta1/(beta1-1))*I_T*(r-alpha)/Ratio;

    V_fun           = @(P) P.*Ratio./(r-alpha)-(I_T/(beta1-1))*((P.*Ratio)/((beta1/(beta1-1))*I_T*(r-alpha)))^beta1;


    Sol_fun         = @(P) (P<P_star_T)*(V_fun (P))+...  % Merge 2 solutions
                            (P>=P_star_T)*I_T;

    % Generate grids

    % Discretization of productivity (log) (index i)
    Pmin            = 0;
    % Productivity grid including PstarT
    Pmax                        = (P_star_T*Ratio*exp(a.*horizon));
    grid_scale                  = Ratio*round(exp(a.*horizon))+1;
    deltaP                      = (P_star_T-Pmin)/precision;
    Pmesh                       = Pmin:deltaP:P_star_T*grid_scale;
    M                           = length(Pmesh)-1; 

    Solution_mesh_buffer{t} = zeros(N+1,M+1);    

    % Time vector
    Tmesh                       = tmax:-deltat:tmin;                            % Descending order (CAUTION!)


    % Step 2: Evaluate R(t) (Time moving Barrier)
    %

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Set: Buffer for time and productivity %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % Set: buffers for V(i,j), productivity, time
    Solution_mesh               = Solution_mesh_buffer{t};
    Solution_mesh(:)            = NaN;                                          % for test purpose only! 

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Set: Terminal and boundary conditions %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % Terminal conditions at t=T
    for i = 1:length(Pmesh)
        if t == N_T
            P                       = Pmesh(i); 
            SolT                    = Sol_fun(P);   
            Solution_mesh(1,i)      = SolT;
        else
            P                       = Pmesh(i); 
            SolT                    = Sol_fun(P*Ratio);   
            Solution_mesh(1,i)      = SolT;
            if isnan(Solution_mesh(1,i)) == 1
            Solution_mesh(1,i)      = I_mesh(end);
            end
        end
    end

    % Boundary conditions at P=Pmin and P=Pmax (loop over t (time))
    for j = 1:length(Tmesh)
        Solution_mesh(j,M+1)    = I_mesh(end+1-j);          % BC at P = Pmax ---> S(Pmax) = I
        Solution_mesh(j,1)      = 0;          % BC at P = Pmin ---> S(Pmin) = 0
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Build: Generating functions and tridiagonal matrix %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % generating function for the linear system (in state space )
    fun_a               = @(i) 0.5*deltat*(alpha*i-sigma^2*i^2);                   % coef
    fun_b               = @(i) 1+(sigma^2*i^2+r)*deltat;                % coef
    fun_c               = @(i) -0.5*(sigma^2*i^2+alpha*i)*deltat;                  % coef
    fun_d               = @(i) (i*deltaP)*deltat;                          % constant (CAUTION! fun_d is time dependent if flag_epl == 1)

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

    %omega                       = 1.2;                                         % Relaxation parameter (1 = Gauss-Seidel)
    tolerance                   = 1e-3;

    % loop over time (except for the terminal date that is already known). Last
    % iteration will fill the last row of the matrix.

    max_iter                    = 200;
    check_iter                  = zeros(N,1);

    for j = 1:N
    %j
        % Set RHS (incl. constants terms)
        vec_consts              = zeros(M-1,1);
        vec_consts(1,1)         = fun_a(0)*Solution_mesh(j+1,1)-Dconsts(2);
        vec_consts(M-1,1)       = fun_c(M)*Solution_mesh(j+1,M+1)-Dconsts(M);
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
              x(i)      = min(omega*x(i)+(1-omega)*x0(i),I_mesh(end-j));         % Check for Barrier
           end
           error    = norm(x-x0);
           x0       = x;

        end
        check_iter(j)                   = n_iter; 
        Solution_mesh(j+1,(2:end-1))  = x;


    end

    % Check for barrier (loop over t)
    Barrier      = zeros(N+1,1);
    for i = 1:N+1
        index         = find(Solution_mesh(i,:)>=I_mesh(end+1-i),1,'first');
        Barrier(i)    = Pmesh(index);
    end
                                   
  
    Bt=flipud(Barrier);
end