'use client'

import { Center, useColorMode } from '@chakra-ui/react'
import { Auth } from '@saas-ui/auth'
import { Link } from '@saas-ui/react'
import { BackgroundGradient } from 'components/gradients/background-gradient'
import { PageTransition } from 'components/motion/page-transition'
import { Section } from 'components/section'
import { NextPage } from 'next'
import * as Icons from 'react-icons/fa'

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

const Login: NextPage = () => {
  const { colorMode } = useColorMode()
  const isDark = colorMode === 'dark'

  return (
    <Section 
      height="calc(100vh - 200px)" 
      innerWidth="container.sm"
      position="relative"
      overflow="hidden"
    >
      <BackgroundGradient 
        zIndex="-1" 
        isDark={isDark}
      />

      <Center 
        height="100%" 
        pt="20"
        position="relative"
        zIndex="1"
      >
        <PageTransition width="100%">
          <Auth
            view="login"
            providers={providers}
            signupLink={<Link href="/signup">Sign up</Link>}
            borderRadius="xl"
            boxShadow="xl"
            bg={isDark ? 'gray.800' : 'white'}
            p={8}
          />
        </PageTransition>
      </Center>
    </Section>
  )
}

export default Login
