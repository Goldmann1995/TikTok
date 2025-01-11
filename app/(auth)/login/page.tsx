'use client'

import { Center, useColorMode } from '@chakra-ui/react'
import { Link } from '@saas-ui/react'
import { BackgroundGradient } from 'components/gradients/background-gradient'
import { PageTransition } from 'components/motion/page-transition'
import { Section } from 'components/section'
import { NextPage } from 'next'
import { supabaseClient } from '@/lib/supabase-client'
import * as Icons from 'react-icons/fa'
import { 
  Box, 
  Stack, 
  Text, 
  Button, 
  Input, 
  FormControl, 
  FormLabel 
} from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import NextLink from 'next/link'
import { Logo } from '#data/logo'
import siteConfig from '#data/config'

const GoogleIcon = () => <Icons.FaGoogle />
const GithubIcon = () => <Icons.FaGithub />

// const providers = {
//   google: {
//     name: 'Google',
//     icon: GoogleIcon
//   },
//   github: {
//     name: 'Github',
//     icon: GithubIcon,
//     variant: 'solid',
//   },
// }

const Login: NextPage = () => {
  const { colorMode } = useColorMode()
  const isDark = colorMode === 'dark'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    const checkUser = async () => {
      const { data: { user } } = await supabaseClient.auth.getUser()
      if (user) {
        window.location.href = `/${user.id}`
      }
    }
    checkUser()
  }, [])

  return (
    <Section height="calc(100vh - 200px)" innerWidth="container.sm" position="relative" overflow="hidden">
      <BackgroundGradient zIndex="-1" isDark={isDark} />
      
      <Center height="100%" pt="20" position="relative" zIndex="1">
        <PageTransition width="100%">
          <Box 
            width="100%" 
            p={8}
            bg={isDark ? 'gray.800' : 'white'}
            borderRadius="xl"
            boxShadow="xl"
          >
            <Stack spacing={4}>
              <Text color={isDark ? 'white' : 'black'} fontSize="3xl" fontWeight="bold" textAlign="center">
                登录
              </Text>
              {error && (
                <Text color="red.500" fontSize="sm" textAlign="center">
                  {error}
                </Text>
              )}
              {success && (
                <Text color="green.500" fontSize="sm" textAlign="center">
                  {success}
                </Text>
              )}
              <FormControl>
                <FormLabel>Email</FormLabel>
                <Input 
                  type="email" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Password</FormLabel>
                <Input 
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </FormControl>
              <Button
                isLoading={isLoading}
                onClick={() => {
                  setIsLoading(true)
                  setError('')
                  setSuccess('')
                  
                  supabaseClient.auth.signInWithPassword({
                    email,
                    password,
                  })
                  .then(({ data, error }) => {
                    if (error) throw error
                    setSuccess('登录成功！')
                    // 可以在这里添加重定向逻辑
                    window.location.href = `/${data.user.id}`
                  })
                  .catch((error) => {
                    setError(error.message)
                  })
                  .finally(() => {
                    setIsLoading(false)
                  })
                }}
              >
                登录
              </Button>
              
              <Text color="muted" fontSize="sm" textAlign="center">
                还没有账号？{' '}
                <Link href="/signup" color={isDark ? 'white' : 'black'}>
                  立即注册
                </Link>
              </Text>
            </Stack>
          </Box>
        </PageTransition>
      </Center>
    </Section>
  )
}

export default Login
