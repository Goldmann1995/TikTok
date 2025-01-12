'use client'

import { Center, useColorMode } from '@chakra-ui/react'
import { BackgroundGradient } from 'components/gradients/background-gradient'
import { PageTransition } from 'components/motion/page-transition'
import { Section } from 'components/section'
import { Link } from '@saas-ui/react'
import { NextPage } from 'next'
import { supabaseClient } from '@/lib/supabase-client'
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
import { useRouter } from 'next/navigation'

const ResetPassword: NextPage = () => {
  const { colorMode } = useColorMode()
  const isDark = colorMode === 'dark'
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isPasswordRecovery, setIsPasswordRecovery] = useState(false)

  useEffect(() => {
    const { data: authListener } = supabaseClient.auth.onAuthStateChange(async (event, session) => {
      if (event === 'PASSWORD_RECOVERY') {
        setIsPasswordRecovery(true)
      }
    })

    return () => {
      authListener?.subscription.unsubscribe()
    }
  }, [])

  const handleResetPassword = async () => {
    setIsLoading(true)
    setError('')
    setSuccess('')
    
    try {
      const { error } = await supabaseClient.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`
      })
      if (error) throw error
      setSuccess('重置密码邮件已发送，请检查您的邮箱')
    } catch (error: any) {
      setError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdatePassword = async () => {
    setIsLoading(true)
    setError('')
    setSuccess('')

    try {
      const { error } = await supabaseClient.auth.updateUser({
        password: newPassword
      })
      if (error) throw error
      setSuccess('密码更新成功！')
      // 延迟跳转到登录页面
      setTimeout(() => {
        router.push('/login')
      }, 2000)
    } catch (error: any) {
      setError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

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
                {isPasswordRecovery ? '设置新密码' : '重置密码'}
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
              
              {isPasswordRecovery ? (
                <FormControl>
                  <FormLabel>新密码</FormLabel>
                  <Input 
                    type="password" 
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="请输入新密码"
                  />
                </FormControl>
              ) : (
                <FormControl>
                  <FormLabel>邮箱地址</FormLabel>
                  <Input 
                    type="email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="请输入您的注册邮箱"
                  />
                </FormControl>
              )}
              
              <Button
                isLoading={isLoading}
                onClick={isPasswordRecovery ? handleUpdatePassword : handleResetPassword}
              >
                {isPasswordRecovery ? '更新密码' : '发送重置邮件'}
              </Button>
              
              <Text color="muted" fontSize="sm" textAlign="center">
                <Link href="/login" color={isDark ? 'white' : 'black'}>
                  返回登录
                </Link>
              </Text>
            </Stack>
          </Box>
        </PageTransition>
      </Center>
    </Section>
  )
}

export default ResetPassword 