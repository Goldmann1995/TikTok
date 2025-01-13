'use client'

import { Box, Center, Stack, Text, useColorMode, Button, Input, FormControl, FormLabel, InputLeftElement, InputGroup } from '@chakra-ui/react'
import { Link } from '@saas-ui/react'
import { NextPage } from 'next'
import NextLink from 'next/link'
import { Features } from '#components/features'
import { BackgroundGradient } from '#components/gradients/background-gradient'
import { PageTransition } from '#components/motion/page-transition'
import { Section } from '#components/section'
import siteConfig from '#data/config'
import { Logo } from '#data/logo'
import { useState } from 'react'
import { supabase } from '@/components/supabase/supabase'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { EmailIcon, LockIcon } from '@chakra-ui/icons'

const Signup: NextPage = () => {
  const { colorMode } = useColorMode()
  const isDark = colorMode === 'dark'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const router = useRouter()

  useEffect(() => {
    const checkSession = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      if (session?.user) {
        router.push(`/${session.user.id}/fortune`)
      }
    }
    checkSession()
  }, [router])

  const handleSignup = async () => {
    setIsLoading(true)
    setError('')
    setSuccess('')
    
    try {
      const signupResult = await supabase.auth.signUp({
        email,
        password,
        options: {
          emailRedirectTo: `${window.location.origin}/`
        }
      })

      if (signupResult.error) throw signupResult.error
      setSuccess('注册成功！请查看邮箱完成验证。')
    } catch (error: any) {
      setError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

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
          <Box pe="20" flex="1">
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
          <Center height="100vh" flex="1" position="sticky" top={0}>
            <Box 
              width="container.sm" 
              pt="8" 
              px="8"
              bg={isDark ? 'gray.800' : 'white'}
              borderRadius="xl"
              boxShadow="xl"
            >
                <Stack spacing={4}>
                  <Text  color={isDark ? 'white' : 'black'} fontSize="3xl" fontWeight="bold" textAlign="center">
                    {siteConfig.signup.title}
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
                    <InputGroup>
                      <InputLeftElement>
                        <EmailIcon color="gray.500" />
                      </InputLeftElement>
                      <Input 
                        type="email" 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                      />
                    </InputGroup>
                  </FormControl>

                  <FormControl>
                    <FormLabel>Password</FormLabel>
                    <InputGroup>
                      <InputLeftElement>
                        <LockIcon color="gray.500" />
                      </InputLeftElement>
                      <Input 
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                      />
                    </InputGroup>
                  </FormControl>

                  <Text color="muted" fontSize="sm">
                    注册即表示您同意我们的{' '}
                    <Link href={siteConfig.termsUrl} color={isDark ? 'white' : 'black'}>
                      服务条款
                    </Link>{' '}
                    and{' '}
                    <Link href={siteConfig.privacyUrl} color={isDark ? 'white' : 'black'}>
                      隐私政策
                    </Link>
                  </Text>
                  <Button
                    isLoading={isLoading}
                    onClick={handleSignup}
                  >
                    注册
                  </Button>
                  <Text color="muted" fontSize="sm">
                    已有账号？
                    <Link href="/login" color={isDark ? 'white' : 'black'}>
                      登录
                    </Link>
                  </Text>
                  
                </Stack>
            </Box>
          </Center>
        </Stack>
      </PageTransition>
    </Section>
  )
}

export default Signup
