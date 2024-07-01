library(DiagrammeR)
library(DiagrammeRsvg)
library(rsvg)

graph <- '
digraph G {
    node [shape=rect, style="rounded", fontsize=20];

    vc [label="Crop\n Data", shape=circle];
    vh [label="Animal\n Data", shape=circle];
    A [label="Parameters\n Definition", shape=doubleoctagon];
    B [label="Encoded\n parameters for\n API requests"];
    C [label="Fetch and\n Process Request", shape=doubleoctagon];
    D [label="Animal County\n Data from API"];
    F [label="Animal State\n Data from API"];
    E [label="Crop County \nData from API"];
    G [label="Crop State\n Data from API"];
    H [label="Data Refining\n Interpolation", shape=doubleoctagon];
    DE [label="Refined Animal\n Data"];
    ED [label="Refined Crop\n Data"];
    I [label="IFEWs Animal\n County Data"];
    J [label="IFEWs Crops\n County Data"];
    
    DA [label="Fertilizer Application\n Rates [32]\n 4x4km2 grid"];
    DB [label="Clip Data with\n Iowa Boundary"];
    DC [label="Convert Raster to\n Point Shapefile"];
    DD [label="Compute Mean Values\n for each County"];
    DF [label="Iowa CN\n for each County"];

    z [label="Variable\n Nitrogen Calculation", shape=doubleoctagon];
    za [label="CN", shape=circle];
    zb [label="GN", shape=circle];
    zc [label="FN", shape=circle];
    zd [label="MN", shape=circle];
    zns [label="Nitrogen\n Surplus", shape=doublecircle];

    vc -> A;
    vh -> A;
    A -> B [label="USDA\n QuickStats\n API"];
    B -> C;
    C -> D;
    C -> F;
    C -> E;
    C -> G;
    D -> H [label="Deal w/\n Suppressed Data"];
    E -> H [label="Deal w/\n Suppressed\n Data"];
    F -> H;
    G -> H;
    H -> DE;
    H -> ED;
    DE -> I;
    ED -> J;
    DA -> DB;
    DB -> DC;
    DC -> DD;
    DD -> DF;
    DF -> z;
    J -> z;
    I -> z;
    z -> za;
    z -> zb;
    z -> zc;
    z -> zd;
    za -> zns [label="+"]; 
    zb -> zns [label="-"];
    zc -> zns [label="+"]; 
    zd -> zns [label="+"]; 
}
'

# Render the graph to SVG
svg_code <- export_svg(grViz(graph))

# Save the SVG file
writeLines(svg_code, "C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig1_data_process.svg")

rsvg_png("C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig1_data_process.svg", "C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig1_data_process.png", width = 600, height = 1362)

# Render the graph using DiagrammeR
grViz(graph)

#GREAT VISUALIZATION TOOL http://magjac.com/graphviz-visual-editor/