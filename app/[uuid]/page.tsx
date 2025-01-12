'use client'
import { Box, Container, Heading, Text } from '@chakra-ui/react'
import { supabase } from '@/components/supabase/supabase'
import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
const UserReport = ({
  params
}: {
  params: { uuid: string }
}) => {
    const [user, setUser] = useState<any>(null)
    const router = useRouter()
    
    const checkUser = async () => {
        const { data: { session } } = await supabase.auth.getSession()
        if (!session) {
          router.push('/login')
          return
        }
        
        // 验证 URL 中的 uuid 是否匹配当前登录用户
        if (session.user.id !== params.uuid) {
          router.push('/login')
          return
        }
        
        setUser(session.user)
        // router.push(`/${user.id}/fortune`)
    }
      
    // 使用 useEffect 来处理副作用
    useEffect(() => {
      checkUser()
    }, [])

  return (
    <Container maxW="container.xl" py={8}>
      <Box>
        <Heading size="lg">开启未来说...</Heading>
      </Box>
    </Container>
  )
}

export default UserReport