'use client'

import { Container, VStack, Text, Button, Select, Input } from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/app/store/userStore'
import { supabase } from '@/components/supabase/supabase'
// 添加时辰定义
const timeRanges = [
  "不确定",
  "子时 (23:00-1:00)",
  "丑时 (1:00-3:00)",
  "寅时 (3:00-5:00)",
  "卯时 (5:00-7:00)",
  "辰时 (7:00-9:00)",
  "巳时 (9:00-11:00)",
  "午时 (11:00-13:00)",
  "未时 (13:00-15:00)",
  "申时 (15:00-17:00)",
  "酉时 (17:00-19:00)",
  "戌时 (19:00-21:00)",
  "亥时 (21:00-23:00)"
]

export default function FortuneForm() {
  const router = useRouter()
  const setUserInfo = useUserStore(state => state.setUserInfo)
  const [uuid, setUuid] = useState('')
  
  // 修改用户验证检查，同时获取UUID
  useEffect(() => {
    const checkUser = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      
      if (!session) {
        router.push('/login')
      } else {
        setUuid(session.user.id) // 从用户数据中获取UUID
      }
    }
    
    checkUser()
  }, [router])

  // 获取今天的日期
  const today = new Date().toISOString().split('T')[0]
  
  const [formData, setFormData] = useState(() => {
    // 如果在客户端，尝试从 localStorage 获取保存的数据
    if (typeof window !== 'undefined') {
      const savedData = localStorage.getItem('userFormData')
      if (savedData) {
        return JSON.parse(savedData)
      }
    }
    // 默认值
    return {
      name: '',
      gender: 'female',
      birthDate: today,
      birthTime: '2'
    }
  })

  // 添加保存数据的副作用
  useEffect(() => {
    localStorage.setItem('userFormData', JSON.stringify(formData))
  }, [formData])

  const handleSubmit = async () => {
    // 修改时辰映射，添加"不确定"对应的默认时间（12点）
    const timeMap = {
      "不确定": "12",
      "子时 (23:00-1:00)": "23",
      "丑时 (1:00-3:00)": "1",
      "寅时 (3:00-5:00)": "3",
      "卯时 (5:00-7:00)": "5",
      "辰时 (7:00-9:00)": "7",
      "巳时 (9:00-11:00)": "9",
      "午时 (11:00-13:00)": "11",
      "未时 (13:00-15:00)": "13",
      "申时 (15:00-17:00)": "15",
      "酉时 (17:00-19:00)": "17",
      "戌时 (19:00-21:00)": "19",
      "亥时 (21:00-23:00)": "21"
    };

    try {
      // 解析日期和时间
      const [year, month, day] = formData.birthDate.split('-');
      const hour = timeMap[timeRanges[parseInt(formData.birthTime)]] || '0';
       const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'
      // 发送请求到后端
      const response = await fetch(`${API_BASE_URL}/bazi`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          year: parseInt(year),
          month: parseInt(month),
          day: parseInt(day),
          hour: parseInt(hour),
          name: formData.name,
          gender: formData.gender === 'male' ? 'male' : 'female'
        }),
      });

      if (!response.ok) {
        throw new Error('请求失败: ' + response.status);
      }

      const result = await response.json();

      if (!result || !result.success) {
        throw new Error(result?.error || '分析失败');
      }

      // 保存结果到全局状态
      setUserInfo({
        ...formData,
        gender: formData.gender === 'male' ? 1 : 0,
        lunarBirthDate: result.data.basic.lunar_date,
        age: result.data.basic.current_age,
        reportData: result.data,
        dailyFortune: result.data.daily_fortune
      });

      // 使用从Supabase获取的UUID进行路由跳转
      router.push(`/${uuid}/report`)

    } catch (error) {
      // 这里可以添加错误提示，比如使用 toast
      alert((error as Error).message || '分析失败，请重试');
    }
  }

  return (
    <Container maxW="container.md" py={20}>
      <VStack spacing={6} align="stretch">
        <Text fontSize="2xl" fontWeight="bold" textAlign="center" 
              bgGradient="linear(to-r, purple.500, pink.500)" 
              bgClip="text">
          基本信息
        </Text>

        <VStack 
          spacing={4} 
          p={6} 
          borderRadius="lg" 
          boxShadow="md"
          bg="chakra-body-bg"
          borderWidth="1px"
          borderColor="chakra-border-color"
        >
          <FormField label="称呼">
            <Input
              placeholder="请输入您的称呼"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </FormField>

          <FormField label="性别">
            <Select
              value={formData.gender}
              onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
            >
              <option value="female">女</option>
              <option value="male">男</option>
            </Select>
          </FormField>

          <FormField label="阳历生日">
            <Input
              type="date"
              value={formData.birthDate}
              onChange={(e) => setFormData({ ...formData, birthDate: e.target.value })}
              sx={{
                // 基础样式
                width: '100%',
                height: '40px',
                padding: '0 12px',
                
                // 日期选择器图标
                '::-webkit-calendar-picker-indicator': {
                  backgroundColor: 'transparent',
                  padding: '8px',
                  cursor: 'pointer',
                  borderRadius: '4px',
                  opacity: 0.8,
                  _hover: {
                    opacity: 1
                  }
                },
                
                // 日期编辑区域
                '::-webkit-datetime-edit': {
                  display: 'flex',
                  alignItems: 'center',
                  padding: '0',
                  justifyContent: 'flex-start',
                },
                
                // 年月日字段容器
                '::-webkit-datetime-edit-fields-wrapper': {
                  padding: '0',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'flex-start',
                  width: 'auto',
                },
                
                // 年月日之间的分隔符
                '::-webkit-datetime-edit-text': { 
                  color: 'inherit',
                  padding: '0 2px',
                  opacity: 0.7,
                },
                
                // 年月日字段
                '::-webkit-datetime-edit-year-field, ::-webkit-datetime-edit-month-field, ::-webkit-datetime-edit-day-field': {
                  padding: '0 2px',
                  color: 'inherit',
                },
                
                // Firefox 特定样式
                '@supports (-moz-appearance: none)': {
                  appearance: 'textfield',
                  '&::-webkit-datetime-edit': {
                    display: 'block',
                    textAlign: 'left',
                  },
                },
                
                // Edge/IE 特定样式
                '@supports (-ms-ime-align: auto)': {
                  '&::-webkit-datetime-edit': {
                    display: 'block',
                    textAlign: 'left',
                  },
                },
              }}
            />
          </FormField>

          <FormField label="出生时辰">
            <Select
              value={formData.birthTime}
              onChange={(e) => setFormData({ ...formData, birthTime: e.target.value })}
            >
              {timeRanges.map((time, index) => (
                <option key={index} value={index}>
                  {time}
                </option>
              ))}
            </Select>
            {formData.birthTime === "0" && (
              <Text fontSize="sm" color="gray.500" mt={1}>
                虽然时辰不确定也能进行基础分析，但若能提供准确时辰，我们将为您呈现更全面、更精准的命理解读。系统将默认使用午时（12点）进行计算。
              </Text>
            )}
          </FormField>

          <Button
            w="full"
            mt={4}
            bgGradient="linear(to-r, purple.500, pink.500)"
            color="white"
            _hover={{
              bgGradient: "linear(to-r, purple.600, pink.600)",
              transform: "scale(1.02)"
            }}
            onClick={handleSubmit}
          >
            八字计算
          </Button>
        </VStack>
      </VStack>
    </Container>
  )
}

// 表单字段组件
const FormField = ({ label, children }) => (
  <VStack align="stretch" w="full">
    <Text fontWeight="medium" color="chakra-text">
      {label}
    </Text>
    {children}
  </VStack>
) 