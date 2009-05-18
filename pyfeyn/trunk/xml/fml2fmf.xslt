<!-- XSLT stylesheet to (roughly) convert FeynML to FeynMF -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" />
<xsl:template match="/feynml">
\documentclass{article}
\usepackage{feynmf,hepnames}
\begin{document}
\begin{fmffile}{output-from-feynmf}
%% Transformation: fml2fmf.xslt
<xsl:for-each select="head">
<xsl:for-each select="meta">%% <xsl:value-of select="@name" />: <xsl:value-of select="@value" />
</xsl:for-each>
<xsl:value-of select="description" />
</xsl:for-each>
<xsl:for-each select="diagram">
 \begin{fmfgraph*}(100,100)
   \fmfleft{<xsl:for-each select="leg"><xsl:if test="@sense='incoming' or @sense='anti-incoming'"><xsl:if test="position()!=1">,</xsl:if><xsl:value-of select="@id" /></xsl:if></xsl:for-each>}
   \fmfright{<xsl:for-each select="leg"><xsl:if test="@sense='outgoing' or @sense='anti-outgoing'"><xsl:if test="position()!=1">,</xsl:if><xsl:value-of select="@id" /></xsl:if></xsl:for-each>}
<xsl:for-each select="leg">   \fmf{<xsl:value-of select="@type" /><xsl:if test="@label!=''">,label=<xsl:value-of select="@label" /></xsl:if>}{<xsl:if test="@sense='incoming' or @sense='anti-outgoing'"><xsl:value-of select="@id" />,<xsl:value-of select="@target" /></xsl:if><xsl:if test="@sense='outgoing' or @sense='anti-incoming'"><xsl:value-of select="@target" />,<xsl:value-of select="@id" /></xsl:if>}
</xsl:for-each>
<xsl:for-each select="vertex">   \fmfv{<xsl:if test="@label!=''">label=<xsl:value-of select="@label" /></xsl:if>}{<xsl:value-of select="@id" />}
</xsl:for-each>
<xsl:for-each select="blob">   \fmfblob{<xsl:if test="@label!=''">label=<xsl:value-of select="@label" /></xsl:if>}{<xsl:value-of select="@id" />}
</xsl:for-each>
<xsl:for-each select="propagator">   \fmf{<xsl:value-of select="@type" /><xsl:if test="@label!=''">,label=<xsl:value-of select="@label" /></xsl:if>}{<xsl:value-of select="@source" />,<xsl:value-of select="@target" />}
</xsl:for-each> \end{fmfgraph*}
</xsl:for-each>
\end{fmffile}
\end{document}
</xsl:template>
</xsl:stylesheet>
<!--
 NOTES:
 (1) Positional attributes are not converted. FeynMF's autopositioning is used.
 (2) Some FeynML line types (graviton, gaugino, gluino) are invalid for FeynMF.
 (3) Anisotropic blobs are not available in straight FeynMF.
-->

