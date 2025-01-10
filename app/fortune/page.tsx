'use client'

import { Container, VStack, Text, Button, Select, Input } from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/app/store/userStore'
    
// 添加时辰定义
const timeRanges = [
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
  
  // 获取今天的日期
  const today = new Date().toISOString().split('T')[0]
  
  const [formData, setFormData] = useState({
    name: '',
    gender: 'female',
    birthDate: today,
    birthTime: '2'
  })

  const handleSubmit = async () => {
    // 从时辰文本中提取小时的映射
    const timeMap = {
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

      // 发送请求到后端
      const response = await fetch('/api/bazi', {
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
        reportData: result.data
      });

      // 导航到报告页面
      router.push('/report');

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