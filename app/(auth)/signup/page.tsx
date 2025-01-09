'use client'

import { Box, Center, Stack, Text, useColorMode } from '@chakra-ui/react'
import { Auth } from '@saas-ui/auth'
import { Link } from '@saas-ui/react'
import { NextPage } from 'next'
import NextLink from 'next/link'
import * as Icons from 'react-icons/fa'
import { Features } from '#components/features'
import { BackgroundGradient } from '#components/gradients/background-gradient'
import { PageTransition } from '#components/motion/page-transition'
import { Section } from '#components/section'
import siteConfig from '#data/config'
import { Logo } from '#data/logo'
const GoogleIcon = () => <Icons.FaGoogle />
const GithubIcon = () => <Icons.FaGithub />

const providers = {
  google: {
    name: 'Google',
    icon: GoogleIcon
  },
  github: {
    name: 'Github',
    icon: GithubIcon,
    variant: 'solid',
  },
}

const Signup: NextPage = () => {
  const { colorMode } = useColorMode()
  const isDark = colorMode === 'dark'

  return (
    <Section height="100vh" innerWidth="container.xl">
      <BackgroundGradient
        zIndex="-1"
        width={{ base: 'full', lg: '50%' }}
        left="auto"
        right="0"
        isDark={isDark}
        borderLeftWidth="1px"
        borderColor={isDark ? 'gray.700' : 'gray.200'}
      />
      <PageTransition height="100%" display="flex" alignItems="center">
        <Stack
          width="100%"
          alignItems={{ base: 'center', lg: 'flex-start' }}
          spacing="20"
          flexDirection={{ base: 'column', lg: 'row' }}
        >
          <Box pe="20">
            <NextLink href="/">
              <Logo width="160px" ms="4" mb={{ base: 0, lg: 16 }} />
            </NextLink>
            <Features
              display={{ base: 'none', lg: 'flex' }}
              columns={1}
              iconSize={4}
              flex="1"
              py="0"
              ps="0"
              maxW={{ base: '100%', xl: '80%' }}
              features={siteConfig.signup.features.map((feature) => ({
                iconPosition: 'left',
                variant: 'left-icon',
                ...feature,
              }))}
            />
          </Box>
          <Center height="100%" flex="1">
            <Box 
              width="container.sm" 
              pt="8" 
              px="8"
              bg={isDark ? 'gray.800' : 'white'}
              borderRadius="xl"
              boxShadow="xl"
            >
              <Auth
                view="signup"
                title={siteConfig.signup.title}
                providers={providers}
                loginLink={<Link href="/login">Log in</Link>}
              >
                <Text color="muted" fontSize="sm">
                  By signing up you agree to our{' '}
                  <Link href={siteConfig.termsUrl} color={isDark ? 'white' : 'black'}>
                    Terms of Service
                  </Link>{' '}
                  and{' '}
                  <Link href={siteConfig.privacyUrl} color={isDark ? 'white' : 'black'}>
                    Privacy Policy
                  </Link>
                </Text>
              </Auth>
            </Box>
          </Center>
        </Stack>
      </PageTransition>
    </Section>
  )
}

export default Signup
