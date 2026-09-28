param(
    [string]$OutputPath = (Join-Path $PSScriptRoot "..\assets\images\social-card.png")
)

Add-Type -AssemblyName System.Drawing

$width = 1200
$height = 627
$bitmap = [System.Drawing.Bitmap]::new($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

$background = [System.Drawing.Drawing2D.LinearGradientBrush]::new(
    [System.Drawing.Rectangle]::new(0, 0, $width, $height),
    [System.Drawing.ColorTranslator]::FromHtml("#F3F7FB"),
    [System.Drawing.ColorTranslator]::FromHtml("#DCECF7"),
    20
)
$graphics.FillRectangle($background, 0, 0, $width, $height)

$navy = [System.Drawing.ColorTranslator]::FromHtml("#0F2235")
$blue = [System.Drawing.ColorTranslator]::FromHtml("#0F5F8F")
$teal = [System.Drawing.ColorTranslator]::FromHtml("#007A69")
$muted = [System.Drawing.ColorTranslator]::FromHtml("#4D6680")
$white = [System.Drawing.Color]::White

# Subtle background geometry.
$softBluePen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(32, 15, 95, 143), 2)
$softTealBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(18, 0, 122, 105))
$graphics.FillEllipse($softTealBrush, 760, -120, 560, 560)
$graphics.DrawEllipse($softBluePen, 820, 45, 390, 390)
$graphics.DrawEllipse($softBluePen, 865, 90, 300, 300)
$graphics.DrawEllipse($softBluePen, 910, 135, 210, 210)

# Portfolio label.
$labelBrush = [System.Drawing.SolidBrush]::new($teal)
$labelRect = [System.Drawing.RectangleF]::new(72, 68, 330, 46)
$labelPath = [System.Drawing.Drawing2D.GraphicsPath]::new()
$radius = 22
$labelPath.AddArc($labelRect.X, $labelRect.Y, $radius * 2, $radius * 2, 180, 90)
$labelPath.AddArc($labelRect.Right - ($radius * 2), $labelRect.Y, $radius * 2, $radius * 2, 270, 90)
$labelPath.AddArc($labelRect.Right - ($radius * 2), $labelRect.Bottom - ($radius * 2), $radius * 2, $radius * 2, 0, 90)
$labelPath.AddArc($labelRect.X, $labelRect.Bottom - ($radius * 2), $radius * 2, $radius * 2, 90, 90)
$labelPath.CloseFigure()
$graphics.FillPath($labelBrush, $labelPath)

$labelFont = [System.Drawing.Font]::new("Segoe UI", 16, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$whiteBrush = [System.Drawing.SolidBrush]::new($white)
$labelFormat = [System.Drawing.StringFormat]::new()
$labelFormat.Alignment = [System.Drawing.StringAlignment]::Center
$labelFormat.LineAlignment = [System.Drawing.StringAlignment]::Center
$graphics.DrawString("ENGINEERING & AI PORTFOLIO", $labelFont, $whiteBrush, $labelRect, $labelFormat)

# Main typography.
$nameFont = [System.Drawing.Font]::new("Segoe UI", 60, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$titleFont = [System.Drawing.Font]::new("Segoe UI", 31, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
$bodyFont = [System.Drawing.Font]::new("Segoe UI", 22, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
$domainFont = [System.Drawing.Font]::new("Segoe UI", 20, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$navyBrush = [System.Drawing.SolidBrush]::new($navy)
$mutedBrush = [System.Drawing.SolidBrush]::new($muted)
$blueBrush = [System.Drawing.SolidBrush]::new($blue)

$graphics.DrawString("Habib Apez", $nameFont, $navyBrush, 70, 150)
$graphics.DrawString("Embedded Systems  |  ADAS", $titleFont, $blueBrush, 74, 235)
$graphics.DrawString("Trustworthy AI", $titleFont, $labelBrush, 74, 278)

$bodyFormat = [System.Drawing.StringFormat]::new()
$bodyFormat.Trimming = [System.Drawing.StringTrimming]::Word
$graphics.DrawString(
    "Safety-critical automotive engineering, control systems,`nand applied artificial intelligence.",
    $bodyFont,
    $mutedBrush,
    [System.Drawing.RectangleF]::new(76, 355, 620, 90),
    $bodyFormat
)
$graphics.DrawString("habibapez.github.io", $domainFont, $navyBrush, 76, 515)

# Right-side systems graphic: embedded controller connected to perception nodes.
$chipBrush = [System.Drawing.SolidBrush]::new($navy)
$chipRect = [System.Drawing.RectangleF]::new(860, 225, 180, 150)
$graphics.FillRectangle($chipBrush, $chipRect)
$chipOutline = [System.Drawing.Pen]::new($teal, 5)
$graphics.DrawRectangle($chipOutline, 860, 225, 180, 150)

$chipFont = [System.Drawing.Font]::new("Segoe UI", 22, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$chipFormat = [System.Drawing.StringFormat]::new()
$chipFormat.Alignment = [System.Drawing.StringAlignment]::Center
$chipFormat.LineAlignment = [System.Drawing.StringAlignment]::Center
$graphics.DrawString("AI +`nEMBEDDED", $chipFont, $whiteBrush, $chipRect, $chipFormat)

$connectionPen = [System.Drawing.Pen]::new($blue, 4)
$nodeBrush = [System.Drawing.SolidBrush]::new($teal)
$whitePen = [System.Drawing.Pen]::new($white, 3)
$nodes = @(
    @(790, 155), @(950, 125), @(1110, 190),
    @(790, 445), @(950, 490), @(1110, 425)
)
foreach ($node in $nodes) {
    $x = [int]$node[0]
    $y = [int]$node[1]
    $targetX = if ($x -lt 900) { 860 } elseif ($x -gt 1030) { 1040 } else { 950 }
    $targetY = if ($y -lt 300) { 225 } else { 375 }
    $graphics.DrawLine($connectionPen, $x, $y, $targetX, $targetY)
    $graphics.FillEllipse($nodeBrush, $x - 12, $y - 12, 24, 24)
    $graphics.DrawEllipse($whitePen, $x - 12, $y - 12, 24, 24)
}

# Accent line and footer marker.
$graphics.FillRectangle($labelBrush, 0, 0, $width, 10)
$graphics.FillRectangle($blueBrush, 76, 565, 150, 6)

$outputDirectory = Split-Path -Parent $OutputPath
[System.IO.Directory]::CreateDirectory($outputDirectory) | Out-Null
$bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$background.Dispose()
$softBluePen.Dispose()
$softTealBrush.Dispose()
$labelBrush.Dispose()
$labelPath.Dispose()
$labelFont.Dispose()
$whiteBrush.Dispose()
$labelFormat.Dispose()
$nameFont.Dispose()
$titleFont.Dispose()
$bodyFont.Dispose()
$domainFont.Dispose()
$navyBrush.Dispose()
$mutedBrush.Dispose()
$blueBrush.Dispose()
$bodyFormat.Dispose()
$chipBrush.Dispose()
$chipOutline.Dispose()
$chipFont.Dispose()
$chipFormat.Dispose()
$connectionPen.Dispose()
$nodeBrush.Dispose()
$whitePen.Dispose()
$graphics.Dispose()
$bitmap.Dispose()

Write-Output "Created $OutputPath ($width x $height)"
