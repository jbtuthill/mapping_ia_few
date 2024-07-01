library(DiagrammeR)
library(DiagrammeRsvg)
library(rsvg)

graph <- '
digraph G {
    node [shape=rect, fontsize=16, fontname="Times New Roman"];

    C [label="JSON to Features\n(Yearly Crop Data)", shape=ellipse];
    C_desc [label="Convert JSON files for the year 2008\n crop data to feature classes", shape=plaintext];
    D [label="JSON to Features\n(Yearly State Crop Rate)", shape=ellipse];
    D_desc [label="Convert JSON files for the state crop\n rate to feature classes", shape=plaintext];
    E [label="Overlay Layers", shape=ellipse];
    E_desc [label="Perform an overlay (intersection) of the\n converted feature classes", shape=plaintext];
    F [label="Calculate Geometry\nAttributes (Ag_ac)", shape=ellipse];
    F_desc [label="Calculate the geodesic area in acres for\n the intersected features", shape=plaintext];
    G [label="Select Layer By Attribute\n(gridcode=1)", shape=ellipse];
    G_desc [label="Select features where a specific attribute condition\n is met (e.g., gridcode=1, which is for corn)", shape=plaintext];

    // Normal flow up to G_desc
    C -> C_desc [arrowhead="none"];
    C_desc -> D;
    D -> D_desc [arrowhead="none"];
    D_desc -> E;
    E -> E_desc [arrowhead="none"];
    E_desc -> F;
    F -> F_desc [arrowhead="none"];
    F_desc -> G;
    G -> G_desc [arrowhead="none"];
}
'

# Render the graph to SVG
svg_code <- export_svg(grViz(graph))

# Save the SVG file
writeLines(svg_code, "C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig2_1_corn_rate_analysis_workflow.svg")

rsvg_png("C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig2_1_corn_rate_analysis_workflow.svg", "C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig2_1_corn_rate_analysis_workflow.png", width = 600, height = 1362)

# Render the graph using DiagrammeR
grViz(graph)



graph <- '
digraph G {
    node [shape=rect, fontsize=16, fontname="Times New Roman"];

    H [label="Calculate Geometry\nAttributes (Corn_ac)", shape=ellipse];
    H_desc [label="Recalculate geometry for selected features to\n determine corn acreage", shape=plaintext];
    I [label="Summary Statistics", shape=ellipse];
    I_desc [label="Generate summary statistics for the selected features\n grouped by an overlay identifier", shape=plaintext];
    J [label="Add Join", shape=ellipse];
    J_desc [label="Join the summary statistics back to the state\n crop rate feature class", shape=plaintext];
    K [label="Calculate Field\n(CornRate)", shape=ellipse];
    K_desc [label="Compute the corn rate using an expression\n based on the joined data", shape=plaintext];
    L [label="Export Features", shape=ellipse];
    L_desc [label="Export the results to a temporary in-memory location", shape=plaintext];

    // Place H next to G_desc and continue vertically
    { rank=same; 
    // G_desc -> H; 
    }
    H -> H_desc [arrowhead="none"];
    H_desc -> I;
    I -> I_desc [arrowhead="none"];
    I_desc -> J;
    J -> J_desc [arrowhead="none"];
    J_desc -> K;
    K -> K_desc [arrowhead="none"];
    K_desc -> L;
    L -> L_desc [arrowhead="none"];
}
'

# Render the graph to SVG
svg_code <- export_svg(grViz(graph))

# Save the SVG file
writeLines(svg_code, "C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig2_2_corn_rate_analysis_workflow.svg")

rsvg_png("C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig2_2_corn_rate_analysis_workflow.svg", "C:\\Users\\julia\\Box\\JBT PhD\\Projects\\Articles\\Article 1 - IFEWs Data Intro\\Paper\\mapping_ia_few\\visualizations\\vis_png\\fig2_2_corn_rate_analysis_workflow.png", width = 600, height = 1362)

# Render the graph using DiagrammeR
grViz(graph)
