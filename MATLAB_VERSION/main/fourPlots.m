function fourPlots(a, Z, f, r, k, Name)
Z = Z / max(abs(Z(:)));  u = real(Z(:));  v = imag(Z(:));
PhiW = angle(Z);  PhiW = wrapToPi(PhiW - PhiW(1,1));
q = linspace(-pi,pi,512);

Title = {'','','',''};
if k == 1
    Title = {'$a$','$b$','$\varphi$', 'Lissajous'};
end

nexttile(r*(k-1)+1);
[~, ecc] = calculateEccentricity(real(Z), imag(Z));
text(0.8,0.5, sprintf('%s,\n ecc=%.4f', Name, ecc), ...
    'HorizontalAlignment','center'); axis off

nexttile(r*(k-1)+2);
h = imshow(a/max(a(:)), [0 1]);
[rows, cols, ~] = size(get(h, 'CData'));
rectangle('Position', [0.5, 0.5, cols, rows], 'EdgeColor', 'k', 'LineWidth', 0.5);
title(Title{1},'Interpreter','latex')

nexttile(r*(k-1)+3);
imshow(abs(Z), [0 1])
[rows, cols, ~] = size(get(h, 'CData'));
rectangle('Position', [0.5, 0.5, cols, rows], 'EdgeColor', 'k', 'LineWidth', 0.5);
title(Title{2},'Interpreter','latex')

nexttile(r*(k-1)+4);
imshow(PhiW, [-pi pi])
[rows, cols, ~] = size(get(h, 'CData'));
rectangle('Position', [0.5, 0.5, cols, rows], 'EdgeColor', 'k', 'LineWidth', 0.5);
title(Title{3},'Interpreter','latex')

nexttile(r*(k-1)+5);
scatter(u,v,[],[0.67 0.67 0.67],'Filled'); box on; hold on
axis(1.1*[-1 1 -1 1]); axis square; xticks(-1:1); yticks(-1:1);
plot(cos(q),sin(q),'--k','LineWidth',1); hold off; grid minor
ax = gca; ax.XAxisLocation = 'origin'; ax.YAxisLocation = 'origin';
xticklabels({''}); yticklabels({''});
title(Title{4},'Interpreter','latex');

nexttile(f*r+2); imshow(ones(size(a)),[0 1])
c = colorbar('Location','north');
c.Position(3) = 0.9*c.Position(3);
c.Position(4) = 0.5*c.Position(4);

nexttile(f*r+3); imshow(ones(size(a)),[0 1])
c = colorbar('Location','north');
c.Position(3) = 0.9*c.Position(3);
c.Position(4) = 0.5*c.Position(4);

nexttile(f*r+4); imshow(pi*ones(size(a)),[-pi pi])
c = colorbar('Location','north');
c.Ticks = [-3,0,3]; c.TickLabels=({'-3','0','3'});
c.Position(3) = 0.9*c.Position(3);
c.Position(4) = 0.5*c.Position(4);

nexttile(f*r+5); imshow(ones(size(a)), [0 1])
text(size(a,1)/2, size(a,2)/4, '-- Unit circle', 'HorizontalAlignment','center')

fontsize(12,"points")
end
