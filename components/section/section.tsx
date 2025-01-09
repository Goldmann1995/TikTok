import {
  chakra,
  useMultiStyleConfig,
  omitThemingProps,
  Container,
  ThemingProps,
  StyleProps,
  HTMLChakraProps,
  Box,
} from '@chakra-ui/react'

export interface SectionProps
  extends HTMLChakraProps<'div'>,
    ThemingProps<'Section'> {
  children: React.ReactNode
  innerWidth?: StyleProps['width']
}

export const Section: React.FC<SectionProps> = (props) => {
  const { children, innerWidth = 'container.lg', className, ...rest } = props

  return (
    <Box
      py={{ base: 8, md: 12 }}
      position="relative"
      {...rest}
    >
      <Container
        height="full"
        maxW={innerWidth}
      >
        {children}
      </Container>
    </Box>
  )
}
