import { Box } from '@chakra-ui/react'

export const BackgroundGradient = ({ hideOverlay, isDark = false, ...props }: any) => {
  // 定义颜色配置
  const colors = {
    primary: isDark ? '#2D3748' : '#4A5568',     // gray.800 : gray.700
    secondary: isDark ? '#D53F8C' : '#ED64A6',   // pink.600 : pink.500
    cyan: isDark ? '#00A3C4' : '#00B5D8',        // cyan.600 : cyan.500
    teal: isDark ? '#2C7A7B' : '#319795'         // teal.600 : teal.500
  }

  let fallbackBackground = `
    radial-gradient(at top left, ${colors.primary} 30%, transparent 80%), 
    radial-gradient(at bottom, ${colors.secondary} 0%, transparent 60%), 
    radial-gradient(at bottom left, ${colors.cyan} 0%, transparent 50%),
    radial-gradient(at top right, ${colors.teal}, transparent), 
    radial-gradient(at bottom right, ${colors.primary} 0%, transparent 50%)
  `

  let gradientOverlay = `linear-gradient(0deg, ${
    isDark ? '#171923' : '#FFFFFF'
  } 60%, rgba(0, 0, 0, 0) 100%)`

  return (
    <Box
      backgroundImage={fallbackBackground}
      backgroundBlendMode="saturation"
      position="absolute"
      top="0"
      left="0"
      zIndex="0"
      opacity={isDark ? '0.5' : '0.3'}
      height="100vh"
      width="100%"
      overflow="hidden"
      pointerEvents="none"
      {...props}
    >
      <Box
        backgroundImage={!hideOverlay ? gradientOverlay : undefined}
        position="absolute"
        top="0"
        right="0"
        bottom="0"
        left="0"
        zIndex="1"
      />
    </Box>
  )
}
