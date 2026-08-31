clearvars; clc;

samplesDir = fullfile(fileparts(mfilename('fullpath')), '..', 'Samples', 'FPP');
files = dir(fullfile(samplesDir, 'synth*.png'));

[~, ord] = sort(str2double(regexp({files.name}, '\d+', 'match', 'once')));
files = files(ord);

selectedIndices = [1, 8, 18, 21, 27];
files = files(selectedIndices);
N = numel(files);

for n = N:-1:1
    Ixy(:,:,n) = imread(fullfile(samplesDir, files(n).name));
end

Ixy = mat2gray(Ixy);

Tol = 1E-4;  maxIter = 60;
tic; [Z_B, a_B] = bruning_func(Ixy); toc

tic; [Z_KK, a_KK] = Kim_Kong_func(Ixy, maxIter, Tol); toc
tic; [Z_AIA, a_AIA] = AIA_Wang(Ixy, maxIter, Tol); toc
tic; [Z_PCA] = pca_func(Ixy); toc
a_PCA = mat2gray(mean(Ixy, 3));
tic; [Z_UPSA, a_UPSA] = UPSA_func(Ixy); toc

%%
h2 = figure(2); set(h2,'Color','white');
set(h2,'Units','normalized','OuterPosition',[0 0 1 1]);
h2.WindowState = 'maximized';

tiledlayout(6,5,'TileSpacing','tight','Padding','tight');
fourPlots(a_B, Z_B, 5,5,1, 'Bruning');
fourPlots(a_KK, Z_KK, 5,5,2, 'K&K');
fourPlots(a_AIA, Z_AIA, 5,5,3,'AIA');
fourPlots(a_PCA, conj(Z_PCA), 5,5,4, 'PCA');
fourPlots(a_UPSA, conj(Z_UPSA), 5,5,5, 'UPSA');

exportgraphics(gcf,'Test.png','Resolution',300,'ColorSpace','gray')
trimWhiteRegions('Test.png', 'Trimmed.png', 255, 5)
winopen('Trimmed.png');
