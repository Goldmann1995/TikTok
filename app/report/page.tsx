'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/app/store/userStore'
import { Container, VStack, Box, Text, Grid, Button, Flex, Icon, Spinner, useToast, Radio, RadioGroup, Stack,Textarea, FormControl, FormLabel, useColorModeValue  } from '@chakra-ui/react'
import { FaBirthdayCake, FaClock, FaMoon, FaUser } from 'react-icons/fa'
import './styles.css' // 引入 CSS 文件

const wuxingColors = {
  金: 'wuxing-gold',
  木: 'wuxing-wood',
  水: 'wuxing-water',
  火: 'wuxing-fire',
  土: 'wuxing-earth',
}

const ganWuxing = {
  甲: '木', 乙: '木',
  丙: '火', 丁: '火',
  戊: '土', 己: '土',
  庚: '金', 辛: '金',
  壬: '水', 癸: '水',
}

const zhiWuxing = {
  寅: '木', 卯: '木',
  巳: '火', 午: '火',
  辰: '土', 戌: '土', 丑: '土', 未: '土',
  申: '金', 酉: '金',
  子: '水', 亥: '水',
}

export default function Report() {
  const router = useRouter()
  const userInfo = useUserStore(state => state)
  const [isLoading, setIsLoading] = useState(false)
  const toast = useToast()
  const [selectedTopic, setSelectedTopic] = useState('comprehensive')
  const [specialQuestion, setSpecialQuestion] = useState('')

  const bgGradient = useColorModeValue(
    'linear(to-br, pink.50, purple.50)',
    'linear(to-br, purple.900, blue.900)'
  )
  const boxBg = useColorModeValue('whiteAlpha.900', 'whiteAlpha.100')
  const borderColor = useColorModeValue('pink.100', 'whiteAlpha.200')
  const tableBg = useColorModeValue('white', 'gray.800')
  const tableHoverBg = useColorModeValue('pink.50', 'whiteAlpha.50')
  const textColor = useColorModeValue('gray.600', 'gray.300')
  const textareaBg = useColorModeValue('white', 'whiteAlpha.100')
  const textareaBorderColor = useColorModeValue('pink.100', 'whiteAlpha.300')
  const textareaBorderHoverColor = useColorModeValue('pink.200', 'whiteAlpha.400')
  const textareaBorderFocusColor = useColorModeValue('pink.300', 'whiteAlpha.500')

  useEffect(() => {
    if (!userInfo.reportData) {
      router.push('/fortune')
    }
  }, [userInfo, router])

  if (!userInfo.reportData) {
    return null
  }

  const baziData = [
    userInfo.reportData.bazi.year,
    userInfo.reportData.bazi.month,
    userInfo.reportData.bazi.day,
    userInfo.reportData.bazi.time,
  ]

  const dayunData = userInfo.reportData.analysis.dayuns.map((dayun, index) => {
    const [gan, zhi] = dayun.split('')
    const startAge = userInfo.reportData.basic.start_age
    const startYear = parseInt(userInfo.reportData.basic.solar_date)
    return {
      gan,
      zhi,
      age: `${startAge + index * 10}-${startAge + (index + 1) * 10}`,
      year: `${startYear + index * 10}-${startYear + (index + 1) * 10}`,
      isCurrent: false,
    }
  })

  return (
    <Container maxW="container.md" py={20} className="report-container">
      <Box className="card">
        <Flex justify="space-between" align="center" className="card-info">
          <Text className="card-title">{userInfo.reportData.basic.name}的基础信息</Text>
          <Box className="card-badge">
            <Text>
              {userInfo.reportData.basic.gender === '男' ? '乾造' : '坤造'}
            </Text>
          </Box>
        </Flex>

        <Grid className="grid">
          {[
            { label: '阳历', value: userInfo.reportData.basic.solar_date, icon: FaBirthdayCake },
            { label: '时辰', value: userInfo.reportData.basic.birth_time, icon: FaClock },
            { label: '农历', value: userInfo.reportData.basic.lunar_date, icon: FaMoon },
            { label: '年龄', value: `${userInfo.reportData.basic.current_age}岁`, icon: FaUser },
          ].map((item, index) => (
            <Box key={index} className="grid-item">
              <Icon as={item.icon} className="icon" />
              <Box>
                <Text>{item.label}</Text>
                <Text>{item.value}</Text>
              </Box>
            </Box>
          ))}
        </Grid>
      </Box>

      <Box className="card">
        <Text className="card-title">八字命盘</Text>
        <Grid templateColumns="repeat(4, 1fr)" gap={6}>
          {['年柱', '月柱', '日柱', '时柱'].map((pillar, index) => {
            const pillarData = baziData[index]
            return (
              <VStack key={index}>
                <Text>{pillar}</Text>
                {[pillarData.gan, pillarData.zhi].map((item, i) => (
                  <Box key={i} className={`circle ${wuxingColors[ganWuxing[item] || zhiWuxing[item]]}`}>
                    {item}
                  </Box>
                ))}
              </VStack>
            )
          })}
        </Grid>
      </Box>

      <Box className="card" mt={6}>
        <Text className="card-title">选择解析主题</Text>
        <RadioGroup value={selectedTopic} onChange={setSelectedTopic}>
          <Stack spacing={4} direction={['column', 'row']} wrap="wrap" justify="center">
            <Radio 
              value="comprehensive"
              colorScheme="pink"
              size="lg"
            >
              综合运势
            </Radio>
            <Radio 
              value="career"
              colorScheme="pink"
              size="lg"
            >
              事业发展
            </Radio>
            <Radio 
              value="wealth"
              colorScheme="pink"
              size="lg"
            >
              财运分析
            </Radio>
            <Radio 
              value="relationship"
              colorScheme="pink"
              size="lg"
            >
              感情姻缘
            </Radio>
            <Radio 
              value="health"
              colorScheme="pink"
              size="lg"
            >
              健康运势
            </Radio>
          </Stack>
        </RadioGroup>
      </Box>

      <Box 
        className="card" 
        mt={6}
        bg={boxBg}
        borderRadius="3xl"
        p={8}
        boxShadow="2xl"
        backdropFilter="blur(10px)"
        border="1px solid"
        borderColor={borderColor}
        w="full"
      >
        <FormControl>
          <FormLabel 
            fontWeight="medium" 
            bgGradient="linear(to-r, pink.400, purple.400)"
            bgClip="text"
          >
            特别想了解的问题（选填）
          </FormLabel>
          <Textarea
            value={specialQuestion}
            onChange={(e) => setSpecialQuestion(e.target.value)}
            placeholder="例如：我今年适合跳槽吗？我和现任的感情会稳定吗？..."
            size="md"
            minH="120px"
            bg={textareaBg}
            borderColor={textareaBorderColor}
            _hover={{
              borderColor: textareaBorderHoverColor
            }}
            _focus={{
              borderColor: textareaBorderFocusColor,
              boxShadow: `0 0 0 1px ${textareaBorderFocusColor}`
            }}
            resize="vertical"
          />
        </FormControl>
      </Box>


      <Button
        w="full"
        size="lg"
        bgGradient="linear(to-r, purple.500, pink.500)"
        color="white"
        _hover={{
          bgGradient: "linear(to-r, purple.600, pink.600)",
          transform: "scale(1.02)"
        }}
        isLoading={isLoading}
        loadingText="正在解析命盘..."
        spinner={
          <Spinner
            thickness="4px"
            speed="0.65s"
            emptyColor="whiteAlpha.300"
            color="white"
            size="md"
          />
        }
        onClick={async () => {
          try {
            setIsLoading(true)
            
            // 准备发送的数据
            const requestData = {
              reportData: userInfo.reportData,
              topic: selectedTopic,
              prompts: {
                comprehensive: "请根据八字命盘进行综合运势分析，包括性格特征、事业发展、财运、感情等各个方面。",
                career: "请重点分析八字命盘中关于事业发展的信息，包括职业方向、发展机遇、注意事项等。",
                wealth: "请详细分析八字命盘中的财运信息，包括财运走势、理财建议、投资机会等。",
                relationship: "请重点解析八字命盘中的感情姻缘信息，包括感情运势、桃花运、婚姻建议等。",
                health: "请根据八字命盘分析健康状况，包括需要注意的健康问题、养生建议等。"
              }[selectedTopic],
              specialQuestion: specialQuestion.trim() // 添加特殊问题
            }
            
            const response = await fetch('/api/generate_report', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(requestData)
            });
            
            if (!response.ok) {
              throw new Error('分析请求失败');
            }
            
            const result = await response.json();
            useUserStore.setState({ analysisResult: result });
            router.push('/analysis');
            
          } catch (error: any) {
            console.error('分析失败:', error);
            toast({
              title: '分析失败',
              description: error.message || '请稍后重试',
              status: 'error',
              duration: 3000,
              isClosable: true,
              position: 'top',
            });
          } finally {
            setIsLoading(false)
          }
        }}
      >
        <VStack spacing={1}>
          <Text fontSize="lg">开启命理解析</Text>
          <Text fontSize="xs" opacity={0.9}>滴天髓深度分析</Text>
        </VStack>
      </Button>
    </Container>
  )
}
