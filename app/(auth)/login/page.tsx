'use client'

import { Center, useColorMode, useToast } from '@chakra-ui/react'
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
  FormLabel, 
  Modal, 
  ModalOverlay, 
  ModalContent, 
  ModalHeader, 
  ModalCloseButton, 
  ModalBody, 
  ModalFooter 
} from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'


const Login: NextPage = () => {
  const { colorMode } = useColorMode()
  const isDark = colorMode === 'dark'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [resetEmail, setResetEmail] = useState('')
  const [isResetModalOpen, setIsResetModalOpen] = useState(false)
  const toast = useToast()
  const router = useRouter()

  useEffect(() => {
    const checkUser = async () => {
      const { data: { user } } = await supabaseClient.auth.getUser()
      if (user) {
        window.location.href = `/${user.id}`
      }
    }
    checkUser()
  }, [])

  useEffect(() => {
    supabaseClient.auth.onAuthStateChange(async (event, session) => {
      if (event === "PASSWORD_RECOVERY") {
        const newPassword = prompt("请输入您的新密码：");
        if (newPassword) {
          const { data, error } = await supabaseClient.auth
            .updateUser({ password: newPassword })

          if (data) {
            toast({
              title: "密码更新成功！",
              status: "success",
              duration: 3000,
            })
          }
          if (error) {
            toast({
              title: "密码更新失败",
              description: error.message,
              status: "error",
              duration: 3000,
            })
          }
        }
      }
    })
  }, [toast])

  const handleResetPassword = async (email: string) => {
    setIsLoading(true)
    try {
      const { error } = await supabaseClient.auth.resetPasswordForEmail(email)
      if (error) throw error
      
      toast({
        title: "重置密码邮件已发送",
        description: "请检查您的邮箱",
        status: "success",
        duration: 5000,
      })
      setIsResetModalOpen(false)
    } catch (error: any) {
      toast({
        title: "发送失败",
        description: error.message,
        status: "error",
        duration: 3000,
      })
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
                variant="link"
                size="sm"
                onClick={() => router.push(`/reset-password/${encodeURIComponent(email)}`)}
                color={isDark ? 'white' : 'black'}
                alignSelf="flex-end"
              >
                忘记密码？
              </Button>
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
                    window.location.href = `/${data.user.id}/fortune`
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
              


              <Modal 
                isOpen={isResetModalOpen} 
                onClose={() => setIsResetModalOpen(false)}
              >
                <ModalOverlay />
                <ModalContent>
                  <ModalHeader>重置密码</ModalHeader>
                  <ModalCloseButton />
                  <ModalBody pb={6}>
                    <FormControl>
                      <FormLabel>邮箱地址</FormLabel>
                      <Input 
                        value={resetEmail}
                        onChange={(e) => setResetEmail(e.target.value)}
                        placeholder="请输入您的注册邮箱"
                      />
                    </FormControl>
                  </ModalBody>

                  <ModalFooter>
                    <Button
                      colorScheme="blue"
                      mr={3}
                      isLoading={isLoading}
                      onClick={() => handleResetPassword(resetEmail)}
                    >
                      发送重置邮件
                    </Button>
                    <Button onClick={() => setIsResetModalOpen(false)}>取消</Button>
                  </ModalFooter>
                </ModalContent>
              </Modal>
              
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
