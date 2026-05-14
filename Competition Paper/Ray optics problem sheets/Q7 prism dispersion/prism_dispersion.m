%prism_dispersion
% Model of the dispersion of white light by a glass prism.
%
% LAST UPDATED by Andy French July 2020.

function prism_dispersion
global d

d.alpha = 60;  %Apex angle of prism /deg
d.dalpha = 1;  %Change in apex angle when a or z keys are pressed
d.thetai = 60; %Angle of incidence of white light from prism normal /deg

%Change in angle of incidence of white light from prism normal /deg
%when up for down arrows are pressed.
d.dthetai = 1;

%Number of frequencies over range 405 to 790 THz
d.N = 500;

%

%Draw default scene
draw_scene;

%Plot deflection angle vs angle of incidence for a variety of alpha angles,
%using the average frequency
deflection_plot;

%%

%Plot deflection angle vs angle of incidence for a variety of alpha angles,
%using the average frequency
function deflection_plot

f = 542.5; %Average visible light frequency /THz
alpha = 10: 5: 80; %Prism apex angle /deg
a = alpha*pi/180;
thetai = linspace(0,90,1000).'; %Angle of incidence /deg
t = thetai*pi/180;
n = nglass(f);  %Refractive index of prism

%Construct arrays of a and t
a = repmat(a,[length(thetai),1]); t = repmat( t,[1,length(alpha)] );

%Transmission angle
z = sin(a).*sqrt( n^2 - sin(t).^2 ) - cos(a).*sin(t);
z( abs(z)>1 ) = NaN;
thetat = asin(z);
delta = t + thetat - a;

%Create plot
fig = figure;
icmap(length(alpha)); map = colormap; set(gca,'colororder',map );
set(gca,'fontsize',18,'nextplot','add');
plot( t*180/pi, delta*180/pi );
xlabel('Angle of incidence /deg');
ylabel('Deflection angle \delta /deg');
title(['Deflection angle \delta /deg using f=',num2str(f),'THz']);
for k=1:length(alpha)
    lstr{k} = ['\alpha=',num2str(alpha(k)),'^o'];
end
legend(lstr,'location','eastoutside');
grid on; box on; xlim([0,90]); ylim([0,90]);
print( gcf,'deflection.png','-r300','-dpng' );
close(fig);

%%

%Determine ray path and angles through prism given f in THz, apex angle A
%in degrees, angle of incidence theta_i in degrees. Assume prism has sides of
%unit slanted lengths. f and A are constants, theta_i can be a matrix.
function p = solve_prism_rays( theta_i,f,A )

%Copnvert prism apex and incidence angles to radians
A = A*pi/180; t = theta_i*pi/180;

%Determine refractive index of glass prism
n = nglass(f);

%Determine maximum angle of incidence before total internal reflectio
%occurs at exit glass-air interface
thetamax = asin( sqrt( (cos(A))^2 + ( n*sin(A) )^2 - 1 ) - cos(A) );

%Determine internal angles and coordinates of ray points a and b
phi = pi/2 - A/2; a = t - A/2;
xa = -cos(a) - 0.5*cos(phi); ya = 0.5*sin(phi);
xb = -0.5*cos(phi); yb = 0.5*sin(phi);

%Determine refraction angle and hence coordinates of point c
B = asin( sin(t)/n ); b = A/2 - B;
xc = 0.5*( sin(phi) +cos(phi)*tan(b) )./( tan(phi) - tan(b) );
yc = -tan(phi)*xc + sin(phi);
ignore = yc<0;
xc(ignore) = NaN; yc(ignore) = NaN;

%Determine angle of transmission (out of prism) and overall deflection of
%incident ray
theta_t = asin( n*sin( A-B ) ); delta = t + theta_t - A;
ignore = abs( n*sin( A-B ) ) > 1;
theta_t(ignore) = NaN;
delta(ignore) = NaN;

%Determine coordinates of exit ray point d
e = theta_t -A/2;
xd = xc +cos(e); yd = yc - sin(e);

%Define outputs
p.ray_x = [xa,xb,xc,xd]; p.ray_y = [ya,yb,yc,yd];
p.theta_t_deg = 180*theta_t/pi;
p.delta_deg = delta*180/pi;
p.theta_max_deg = 180*thetamax/pi;

%%

%Sellmeier equation for the refractive index n of glass
%(BK7 Crown glass). f is frequency of light /THz
function n = nglass(f)
%Determine in vacuum wavelength /microns
lambda = 2.998e8./(f*1e12);
lambda = lambda*1e6;

%Sellmeier coefficients
a = [1.03961212, 0.231792344,1.01146945];
b = [0.00600069867,0.0200179144,103.560653];

%Sellmeier sum
s = zeros(size(f));
for n=1:numel(a);
    s = s + a(n)*( lambda.^2 )./ ( ( lambda.^2 ) - b(n) );
end

%Determine refractive index
n = sqrt( s + 1 );

%%

%RGB colour from light frequency /THz
function RGB = RGB_from_f(f)
F = [405,480,510,530,600,620,680];
R = [1,1,1,0,0,0,137/255]; G = [0,127/255,1,1,1,0,0];
B = [0,0,0,0,1,1,1];
RGB = zeros( numel(f),3 );
r = interp1( F,R,f ); g = interp1( F,G,f ); b = interp1( F,B,f );
RGB(:,1) = r(:); RGB(:,2) = g(:); RGB(:,3) = b(:);

%%

%Create ray plot
function draw_scene
global d

%Create figure
d.fig = figure('color',[0,0,0],...
    'units','normalized','position',[0.05,0.02,0.9,0.9],...
    'KeyPressFcn',@keypress,'renderer','painters');
axis equal; axis off; hold on;
xlim([-2,2]);ylim([-1,1]); axis manual;

%Draw prism, with unit length slanted sides
A = d.alpha*pi/180; phi = pi/2 - A/2;
xp = [-cos(phi),0,cos(phi),-cos(phi)];
yp = [0,sin(phi),0,0];
d.prism = plot( xp,yp,'w-','linewidth',2 );

%Define initial white light ray path
a = d.thetai*pi/180 - A/2;
xw = [ -cos(a) - 0.5*cos(phi),-0.5*cos(phi)];
yw = [0.5*sin(phi)-sin(a),0.5*sin(phi)];
d.white = plot( xw,yw,'w-','linewidth',2 );

%Plot normal to more clearly show angle of incidence
xn = [-0.5*cos(phi)-0.2*sin(phi), -0.5*cos(phi)+0.2*sin(phi)];
yn = [0.5*sin(phi)+0.2*cos(phi), 0.5*sin(phi)-0.2*cos(phi)];
d.normal = plot( xn,yn,'w--','linewidth',2 );

%Define range of frequencies /THz
d.f = linspace( 405,680,d.N );

%Solve prism for each frequency, and plot ray path from B to D
ray_x = NaN( 3,d.N); ray_y = NaN( 3,d.N ); RGB = zeros( d.N,3 );
for k=1:d.N
    p = solve_prism_rays( d.thetai,d.f(k),d.alpha );
    RGB(k,:) = RGB_from_f( d.f(k) );
    ray_x(:,k) = p.ray_x(2:4); ray_y(:,k) = p.ray_y(2:4);
end
set(gca,'colororder',RGB);
d.rays = plot( ray_x,ray_y,'linewidth',2 );

%Plot normal at point C for lowest frequency
xc = ray_x(2,1); yc = ray_y(2,1);
xn = [xc-0.2*sin(phi), xc+0.2*sin(phi)];
yn = [yc-0.2*cos(phi), yc+0.2*cos(phi)];
d.normalC = plot( xn,yn,'w--','linewidth',2 );

%Set axes title
d.title = title( ['\theta_i = ',num2str(d.thetai),...
    '^o, \alpha = ',num2str(d.alpha),'^o'],'fontsize',32,'color',[1,1,1] );

%%

%Update ray plot
function update_scene
global d

%Draw prism, with unit length slanted sides
A = d.alpha*pi/180; phi = pi/2 - A/2;
xp = [-cos(phi),0,cos(phi),-cos(phi)];
yp = [0,sin(phi),0,0];
set( d.prism,'xdata',xp,'ydata',yp );

%Define initial white light ray path
a = d.thetai*pi/180 - A/2;
xw = [ -cos(a) - 0.5*cos(phi),-0.5*cos(phi)];
yw = [0.5*sin(phi)-sin(a),0.5*sin(phi)];
set( d.white,'xdata',xw,'ydata',yw );

%Plot normal to more clearly show angle of incidence
xn = [-0.5*cos(phi)-0.2*sin(phi), -0.5*cos(phi)+0.2*sin(phi)];
yn = [0.5*sin(phi)+0.2*cos(phi), 0.5*sin(phi)-0.2*cos(phi)];
set( d.normal,'xdata',xn,'ydata',yn );

%Solve prism for each frequency, and plot ray path from B to D
ray_x = NaN( 3,d.N); ray_y = NaN( 3,d.N ); RGB = zeros( d.N,3 );
for k=1:d.N
    p = solve_prism_rays( d.thetai,d.f(k),d.alpha );
    RGB(k,:) = RGB_from_f( d.f(k) );
    set( d.rays(k),'xdata', p.ray_x(2:4), 'ydata', p.ray_y(2:4) );
    if k==1
        xc = p.ray_x(3); yc = p.ray_y(3);
    end
end

%Plot normal at point C for lowest frequency
xn = [xc-0.2*sin(phi), xc+0.2*sin(phi)];
yn = [yc-0.2*cos(phi), yc+0.2*cos(phi)];
set( d.normalC,'xdata',xn,'ydata',yn );

%Set axes title
set( d.title,'string',['\theta_i = ',num2str(d.thetai),...
    '^o, \alpha = ',num2str(d.alpha),'^o'] )

%Flush graphics buffer
drawnow;

%%

%Plot graph of deflection and angle of transmission vs f for given angle of
%incidence
function plot_deflection_vs_f
global d

%Find angles
theta_t_deg = NaN(1,d.N); delta_deg = NaN(1,d.N);
theta_max_deg = NaN(1,d.N);
for k=1:d.N
    p = solve_prism_rays( d.thetai,d.f(k),d.alpha );
    theta_t_deg(k) = p.theta_t_deg;
    delta_deg(k)  = p.delta_deg;
    theta_max_deg(k)  = p.theta_max_deg;
end

%Transmission angle
fig = figure;
axes('nextplot','add','fontsize',18); grid on; box on;
plot( d.f, theta_t_deg,'linewidth',1 );
xlabel('Frequency /THz');
ylabel('\theta_t /deg');
title(['Transmission angle from normal given \alpha=',...
    num2str(d.alpha),'^o, \theta_i=',num2str(d.thetai),'^o']);
print( fig,['thetat given alpha=',...
    num2str(d.alpha),' thetai=',num2str(d.thetai),'.png'],'-dpng','-r300');
close(fig);

%Maximum angle of incidence
fig = figure;
axes('nextplot','add','fontsize',18); grid on; box on;
plot( d.f, theta_max_deg,'linewidth',1 );
xlabel('Frequency /THz');
ylabel('\theta_{max} /deg');
title(['\theta_{max} given \alpha=',num2str(d.alpha),'^o']);
print( fig,['Theta max given alpha = ',num2str(d.alpha),'.png'],'-dpng','-r300');
close(fig);

%Deflection from incident ray
fig = figure;
axes('nextplot','add','fontsize',18); grid on; box on;
plot( d.f, delta_deg,'linewidth',1);
xlabel('Frequency /THz');
ylabel('Deflection angle \delta /deg');
title(['Deflection angle given \alpha=',num2str(d.alpha),...
    '^o, \theta_i=',num2str(d.thetai),'^o']);
print( fig,['delta given alpha=',num2str(d.alpha),...
    ' thetai=',num2str(d.thetai),'.png'],'-dpng','-r300');
close(fig);

%%

%Plot graph of deflection and angle of transmission vs angle of incidence
%using average frequency
function plot_deflection_vs_theta_i
global d

%Find angles
N = 500;
thetai = linspace(0,90,N);
theta_t_deg = NaN(1,N); delta_deg = NaN(1,N); f = mean(d.f);
for k=1:N
    p = solve_prism_rays( thetai(k),f,d.alpha );
    theta_t_deg(k) = p.theta_t_deg;
    delta_deg(k)  = p.delta_deg;
    theta_max_deg = p.theta_max_deg;
end

%Transmission angle
fig = figure;
axes('nextplot','add','fontsize',18); grid on; box on;
plot( thetai, theta_t_deg,'linewidth',1 ); xlim([0,90]);
ylimits = get(gca,'ylim');
plot( theta_max_deg*[1,1],ylimits,'r--','linewidth',1);
xlabel('Angle of incidence /deg');
ylabel('Transmission angle \theta_t /deg');
title(['\theta_t vs \theta_i given \alpha=',...
    num2str(d.alpha),'^o, f=',num2str(f),'THz. \theta_{max}=',num2str(theta_max_deg,4),'^o.']);
print( fig,['thetat given alpha=',...
    num2str(d.alpha),' vs thetai.png'],'-dpng','-r300');
close(fig);

%Deflection from incident ray
fig = figure;
axes('nextplot','add','fontsize',18); grid on; box on;
plot( thetai, delta_deg,'linewidth',1);  xlim([0,90]);
ylimits = get(gca,'ylim');
plot( theta_max_deg*[1,1],ylimits,'r--','linewidth',1);
xlabel('Angle of incidence /deg');
ylabel('Deflection angle \delta /deg');
title(['Deflection angle given \alpha=',num2str(d.alpha),...
    '^o, f=',num2str(f),'THz. \theta_{max}=',num2str(theta_max_deg,4),'^o.']);
print( fig,['delta given alpha=',num2str(d.alpha),...
    ' vs thetai.png'],'-dpng','-r300');
close(fig);

%%

%Plot a surface of deflection angle vs frequency and angle of incidence
function plot_deflection_surface
global d
N = 100;
theta_t_deg = linspace(0,90,100); f = linspace( 405,680,N );
delta_deg = NaN(N,N);
for i=1:N
    for j=1:N
        p = solve_prism_rays( theta_t_deg(j),f(i),d.alpha );
        delta_deg(i,j)  = p.delta_deg;
    end
end
[f,ti] = meshgrid( f,theta_t_deg );
fig=figure; axes('fontsize',18);
surf( f,ti,delta_deg.');
axis vis3d;
%view(2); ylim([0,90]); xlim([min(d.f),max(d.f)]);
shading interp; icmap; colorbar('fontsize',18);
xlabel('Frequency /THz'); ylabel('\theta_i /deg'); zlabel('Deflection \delta /deg');
title(['Deflection /deg, \alpha=',num2str(d.alpha),'^o']);
print(fig,['Deflection surface alpha=',num2str(d.alpha),'.png'],'-r300','-dpng');
close(fig);

%%

%Interpolates current colormap to yield better graduated shading.
function icmap(varargin)
if nargin==0
N = 1000; %Length of new colormap
else
    N = varargin{1};
end
map = colormap; new_map = ones(N,3); %Get current colormap

%Get size of current colormap and initalise R,G,B vectors
dim = size(map);
R = ones(1,dim(1)); G = ones(1,dim(1)); B = ones(1,dim(1));
RR = ones(1,N); GG = ones(1,N); BB = ones(1,N);

%Populate R,G,B with current colormap
R(:) = map(:,1); G(:) = map(:,2); B(:) = map(:,3);

%Interpolate R,G,B to yield new colour map
x = linspace( 1, dim(1), N );
RR = interp1( 1:dim(1), R, x ); GG = interp1( 1:dim(1), G, x ); BB = interp1( 1:dim(1), B, x );
new_map(:,1) = RR(:); new_map(:,2) = GG(:); new_map(:,3) = BB(:);

%Set colormap to be new map
colormap( new_map );

%%

%Function which executes when a key is pressed
function keypress(fig,evnt)
global d

if strcmp(get(fig,'currentkey'),'downarrow')==1
    d.thetai = d.thetai + d.dthetai;
    if d.thetai > 90; d.thetai = 90; end
elseif strcmp(get(fig,'currentkey'),'uparrow')==1
    d.thetai = d.thetai - d.dthetai;
    if d.thetai < 0; d.thetai = 0; end
elseif strcmp(get(fig,'currentkey'),'a')==1
    d.alpha = d.alpha + d.dalpha;
    if d.alpha > 89; d.alpha = 89; end
elseif strcmp(get(fig,'currentkey'),'z')==1
    d.alpha = d.alpha - d.dalpha;
    if d.alpha < 1; d.alpha = 1; end
elseif strcmp(get(fig,'currentkey'),'p')==1
    plot_deflection_vs_f;
    set( d.title,'fontsize',18 );
    print( gcf,['prism i=',num2str(d.thetai),' alpha=',num2str(d.alpha),'.png'],'-dpng','-r300' );
    set( d.title,'fontsize',32 );
elseif strcmp(get(fig,'currentkey'),'f')==1
    plot_deflection_surface;
elseif strcmp(get(fig,'currentkey'),'t')==1
    plot_deflection_vs_theta_i
end

%Update plot
update_scene;

%End of code