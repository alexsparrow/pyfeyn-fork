<!-- XSLT stylesheet to extract math attributes from FeynML -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" />
<xsl:template match="/feynml">
// Transformation: fml2fmf.xslt
<xsl:for-each select="head">
<xsl:for-each select="meta">// <xsl:value-of select="@name" />: <xsl:value-of select="@value" />
</xsl:for-each>
/*<xsl:value-of select="description" />*/
</xsl:for-each>
<xsl:for-each select="diagram">
 a<xsl:value-of select="@id" /> = <xsl:for-each select="leg">   <xsl:value-of select="@math" />*</xsl:for-each><xsl:for-each select="vertex">   <xsl:value-of select="@math" />*</xsl:for-each><xsl:for-each select="blob">   <xsl:value-of select="@math" />*</xsl:for-each><xsl:for-each select="propagator">   <xsl:value-of select="@math" /><xsl:if test="position()!=last()">*</xsl:if>
</xsl:for-each>;

</xsl:for-each>
</xsl:template>
</xsl:stylesheet>

