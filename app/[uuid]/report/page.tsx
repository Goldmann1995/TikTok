'use client'

import { useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/app/store/userStore'
import { Container, VStack, Box, Text, Grid, Button, Flex,
 Icon, Spinner, useToast, Radio, RadioGroup, Stack, Textarea,
  FormControl, FormLabel, useColorModeValue, CircularProgress, CircularProgressLabel, Progress } from '@chakra-ui/react'
import { FaBirthdayCake, FaClock, FaMoon, FaUser } from 'react-icons/fa'
import { supabase } from '@/components/supabase/supabase'
import './styles.css'

// 五行颜色映射
const wuxingColors = {
  金: 'wuxing-gold',
  木: 'wuxing-wood',
  水: 'wuxing-water',
  火: 'wuxing-fire',
  土: 'wuxing-earth',
}

// 天干五行对应
const ganWuxing = {
  甲: '木', 乙: '木',
  丙: '火', 丁: '火',
  戊: '土', 己: '土',
  庚: '金', 辛: '金',
  壬: '水', 癸: '水',
}

// 地支五行对应
const zhiWuxing = {
  寅: '木', 卯: '木',
  巳: '火', 午: '火',
  辰: '土', 戌: '土', 丑: '土', 未: '土',
  申: '金', 酉: '金',
  子: '水', 亥: '水',
}

// 定义运势数据接口类型
interface DailyFortune {
  scores: {
    love: number;
    wealth: number;
    career: number;
    study: number;
    health: number;
  };
  lucky: {
    color: {
      name: string;
      hex: string;
    };
    numbers: string;
    direction: {
      喜神: string;
      财神: string;
      福神: string;
      贵人: string;
    };
  };
  activities: {
    good: string[];
    bad: string[];
  };
}

// 在组件顶部添加接口定义
interface TimeoutData {
  timerId: NodeJS.Timeout;
  toastId?: string | number;
}

export default function Report() {
  const router = useRouter()
  const userInfo = useUserStore(state => state)
  const [isLoading, setIsLoading] = useState(false)
  const toast = useToast()
  const [uuid, setUuid] = useState('')
  const [selectedTopic, setSelectedTopic] = useState(useUserStore.getState().selectedTopic || 'comprehensive')
  const [specialQuestion, setSpecialQuestion] = useState(useUserStore.getState().specialQuestion || '')
  const [dailyFortune, setDailyFortune] = useState<DailyFortune>(userInfo.dailyFortune);
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
  const [timeoutId, setTimeoutId] = useState<TimeoutData | null>(null)


  useEffect(() => {
    // 如果没有报告数据，重定向到 fortune 页面
    const checkUser = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) {
        router.push('/login')
      }else{
        setUuid(session.user.id)
        if (!userInfo.reportData) {
          router.push(`/${session.user.id}/fortune`)
          return
        }
      }
    }
    
    checkUser()


    // 组件卸载时的清理函数
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId.timerId)
        if (timeoutId.toastId) {
          toast.close(timeoutId.toastId)
        }
      }
      useUserStore.setState({ analysisProgress: 0 })
    }
  }, [userInfo.reportData, router, timeoutId, toast])

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
  console.log(userInfo)

  const handleAnalysis = async () => {
    try {
      setIsLoading(true)
      let currentProgress = 0
      
      // 使用 useRef 来存储 interval ID
      const progressInterval = setInterval(() => {
        currentProgress += Math.random() * 3.5 // 每次增加0-1.5%
        if (currentProgress > 90) {
          currentProgress = 90
          clearInterval(progressInterval)
        }
        // 只有当进度真正改变时才更新状态
        if (currentProgress !== userInfo.analysisProgress) {
          useUserStore.setState({ analysisProgress: Math.min(currentProgress, 90) })
        }
      }, 800)

      // 确保在组件卸载或请求完成时清除定时器
      const cleanup = () => {
        clearInterval(progressInterval)
      }

      // 添加到 timeoutId 中以便清理
      setTimeoutId({
        timerId: progressInterval,
      })
      
      try {
        const requestData = {
          reportData: userInfo.reportData,
          topic: selectedTopic,
          prompts: {
            comprehensive: "请根据八字命盘进行综合运势分析...",
            career: "请重点分析八字命盘中关于事业发展的信息，包括职业方向、发展机遇、注意事项等。",
            wealth: "请详细分析八字命盘中的财运信息，包括财运走势、理财建议、投资机会等。",
            relationship: "请重点解析八字命盘中的感情姻缘信息，包括感情运势、桃花运、婚姻建议等。",
            health: "请根据八字命盘分析健康状况，包括需要注意的健康问题、养生建议等。",
            profession: "请根据八字命盘分析职业发展，包括职业方向、发展机遇、注意事项等。"
          }[selectedTopic],
          specialQuestion: specialQuestion.trim()
        }
        const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'
        const response = await fetch(`${API_BASE_URL}/generate_report`, {
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
        
        // 清理定时器
        cleanup()
        
        // 设置100%进度
        useUserStore.setState({ 
          analysisResult: result,
          analysisProgress: 100 
        })
        
        await new Promise(resolve => setTimeout(resolve, 500))
        router.push(`/${uuid}/analysis`);
        
      } catch (error) {
        cleanup()
        throw error;
      }
      
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
      useUserStore.setState({ analysisProgress: 0 })
    }
  }

  return (
    <Container maxW="container.md" py={20} className="report-container">
      <Box className="card">
        <Flex justify="space-between" align="center" mb={4}>
          <Text className="card-title" fontSize="xl">基础信息</Text>
          <Box px={3} py={1} borderRadius="full" bg="pink.100" color="pink.500">
            <Text fontSize="sm">
              {userInfo.reportData.basic.gender === '男' ? '乾造' : '坤造'}
            </Text>
          </Box>
        </Flex>

        <Grid templateColumns="repeat(4, 1fr)" gap={3}>
          {[
            { label: '阳历', value: userInfo.reportData.basic.solar_date, icon: FaBirthdayCake },
            { label: '时辰', value: userInfo.reportData.basic.birth_time, icon: FaClock },
            { label: '农历', value: userInfo.reportData.basic.lunar_date, icon: FaMoon },
            { label: '年龄', value: `${userInfo.reportData.basic.current_age}岁`, icon: FaUser },
          ].map((item, index) => (
            <Flex key={index} align="center" gap={2} p={2}>
              <Icon as={item.icon} color="pink.400" />
              <VStack align="start" spacing={0}>
                <Text fontSize="xs" color="gray.500">{item.label}</Text>
                <Text fontSize="sm">{item.value}</Text>
              </VStack>
            </Flex>
          ))}
        </Grid>
      </Box>

      <Box className="card">
        <Text className="card-title">八字命盘</Text>
        <Grid templateColumns="auto repeat(4, 1fr)" gap={4}>
          {/* 表头行 */}
          <Box></Box>
          {['年柱', '月柱', '日柱', '时柱'].map((pillar, index) => (
            <Text 
              key={index} 
              textAlign="center" 
              fontWeight="bold" 
              fontSize="2xl"
            >
              {pillar}
            </Text>
          ))}

          {/* 干神行 */}
          <Text pl={2} fontWeight="bold" fontSize="2xl">干神</Text>
          {['year', 'month', 'day', 'time'].map((pillar) => {
            const gan = userInfo.reportData.bazi[pillar].gan;
            return (
              <Text 
                key={pillar} 
                textAlign="center" 
                fontSize="xl"
                className={wuxingColors[ganWuxing[gan]]}
              >
                {userInfo.reportData.bazi[pillar].shen}
              </Text>
            );
          })}

          {/* 天干行 */}
          <Text pl={2} fontWeight="bold" fontSize="2xl">天干</Text>
          {['year', 'month', 'day', 'time'].map((pillar) => {
            const gan = userInfo.reportData.bazi[pillar].gan;
            return (
              <Text 
                key={pillar} 
                textAlign="center" 
                fontSize="xl"
                className={wuxingColors[ganWuxing[gan]]}
              >
                {gan}
              </Text>
            );
          })}

          {/* 地支行 */}
          <Text pl={2} fontWeight="bold" fontSize="2xl">地支</Text>
          {['year', 'month', 'day', 'time'].map((pillar) => {
            const zhi = userInfo.reportData.bazi[pillar].zhi;
            return (
              <Text 
                key={pillar} 
                textAlign="center" 
                fontSize="xl"
                className={wuxingColors[zhiWuxing[zhi]]}
              >
                {zhi}
              </Text>
            );
          })}
          {/* 藏干行 *
          <Text pl={2} fontWeight="bold" fontSize="2xl">藏干</Text>
          {['year', 'month', 'day', 'time'].map((pillar) => (
            <VStack key={pillar} spacing={0} align="center">
              {Object.entries(userInfo.reportData.bazi[pillar].canggan || {}).map(([gan, weight], idx) => (
                <Text 
                  key={idx} 
                  fontSize="xl"
                  className={wuxingColors[ganWuxing[gan]]}
                >
                  {gan}
                </Text>
              ))}
            </VStack>
          ))}

       
          <Text pl={2} fontWeight="bold" fontSize="2xl">支神</Text>
          {['year', 'month', 'day', 'time'].map((pillar) => {
            const zhi = userInfo.reportData.bazi[pillar].zhi;
            return (
              <Text 
                key={pillar} 
                textAlign="center" 
                fontSize="xl"
                className={wuxingColors[zhiWuxing[zhi]]}
              >
                {userInfo.reportData.bazi[pillar].zhi_shens}
              </Text>
            );
          })} */}
        </Grid>
      </Box>


      <Box className="card">
        <Text className="card-title" fontSize="xl">今日运势</Text>
        
        {/* 运势分数 */}
        <Grid templateColumns="repeat(5, 1fr)" gap={4} mb={6}>
          {[
            { 
              label: '爱情运', 
              score: dailyFortune.scores.love, 
              color: 'pink',
              description: dailyFortune.scores.love > 35 
                ? '桃花运旺盛，易获得良缘'
                : '感情需谨慎，不宜轻易承诺'
            },
            { 
              label: '财运', 
              score: dailyFortune.scores.wealth, 
              color: 'yellow',
              description: dailyFortune.scores.wealth > 35
                ? '财源广进，投资顺利'
                : '理财需谨慎，避免冒险投资'
            },
            { 
              label: '事业运', 
              score: dailyFortune.scores.career, 
              color: 'purple',
              description: dailyFortune.scores.career > 35
                ? '贵人相助，事业有成'
                : '事业有阻，需稳扎稳打'
            },
            { 
              label: '学习运', 
              score: dailyFortune.scores.study, 
              color: 'blue',
              description: dailyFortune.scores.study > 35
                ? '思维敏捷，学习顺利'
                : '注意力分散，需要专注'
            },
            { 
              label: '健康运', 
              score: dailyFortune.scores.health, 
              color: 'green',
              description: dailyFortune.scores.health > 35
                ? '精力充沛，身体健康'
                : '注意休息，避免过度劳累'
            },
          ].map((item) => (
            <VStack key={item.label} spacing={2}>
              <CircularProgress 
                value={item.score} 
                color={`${item.color}.400`}
                size="80px"
                thickness="8px"
                trackColor={`${item.color}.50`}
              >
                <CircularProgressLabel 
                  fontSize="md"
                  fontWeight="bold"
                  color={`${item.color}.500`}
                  _dark={{ color: `${item.color}.300` }}
                >
                  {item.score}
                </CircularProgressLabel>
              </CircularProgress>
              <Text 
                fontSize="md" 
                fontWeight="bold"
                color={`${item.color}.500`}
                _dark={{ color: `${item.color}.300` }}
              >
                {item.label}
              </Text>
              <Text
                fontSize="xs"
                color="gray.600"
                _dark={{ color: 'gray.300' }}
                textAlign="center"
                px={2}
              >
                {item.description}
              </Text>
            </VStack>
          ))}
        </Grid>

        {/* 幸运信息 */}
        <Grid templateColumns="repeat(3, 1fr)" gap={4} mb={6}>
          {[
            { 
              label: '幸运色', 
              value: dailyFortune.lucky.color.name,
              bgColor: dailyFortune.lucky.color.hex 
            },
            { label: '幸运数字', value: dailyFortune.lucky.numbers },
            { 
              label: '财星方位', 
              directions: [
                { 
                  god: '财神', 
                  dir: dailyFortune.lucky.direction.财神, 
                  color: 'yellow.500',
                  bgLight: 'yellow.50',
                  bgDark: 'yellow.900',
                  borderLight: 'yellow.200',
                  borderDark: 'yellow.700'
                },
                { 
                  god: '贵人', 
                  dir: dailyFortune.lucky.direction.贵人, 
                  color: 'purple.500',
                  bgLight: 'purple.50',
                  bgDark: 'purple.900',
                  borderLight: 'purple.200',
                  borderDark: 'purple.700'
                },
                { 
                  god: '喜神', 
                  dir: dailyFortune.lucky.direction.喜神, 
                  color: 'pink.500',
                  bgLight: 'pink.50',
                  bgDark: 'pink.900',
                  borderLight: 'pink.200',
                  borderDark: 'pink.700'
                },
                { 
                  god: '福神', 
                  dir: dailyFortune.lucky.direction.福神, 
                  color: 'green.500',
                  bgLight: 'green.50',
                  bgDark: 'green.900',
                  borderLight: 'green.200',
                  borderDark: 'green.700'
                },
              ]
            },
          ].map((item) => (
            <VStack 
              key={item.label}
              p={3} 
              bg="whiteAlpha.900" 
              _dark={{ bg: 'whiteAlpha.200' }}
              borderRadius="lg"
              spacing={2}
              position="relative"
              h="full"
            >
              <Text 
                fontSize="lg" 
                fontWeight="semibold"
                color="gray.700"
                _dark={{ color: 'gray.200' }}
                borderBottom="2px solid"
                borderColor="pink.200"
                pb={1}
              >
                {item.label}
              </Text>
              {item.directions ? (
                <Grid templateColumns="repeat(2, 1fr)" gap={2} w="full">
                  {item.directions.map((direction) => (
                    <Box
                      key={direction.god}
                      p={2}
                      borderRadius="md"
                      bg={direction.bgLight}
                      border="1px solid"
                      borderColor={direction.borderLight}
                      _dark={{ 
                        borderColor: direction.borderDark 
                      }}
                      transition="all 0.2s"
                      _hover={{
                        transform: "scale(1.05)",
                        boxShadow: "sm"
                      }}
                    >
                      <VStack spacing={0}>
                        <Text
                          fontSize="sm"
                          color={direction.color}
                          fontWeight="bold"
                        >
                          {direction.god}
                        </Text>
                        <Text
                          fontSize="md"
                          fontWeight="semibold"
                          color={`${direction.color}`}
                          _dark={{ color: `${direction.color}` }}
                        >
                          {direction.dir}
                        </Text>
                      </VStack>
                    </Box>
                  ))}
                </Grid>
              ) : (
                <Flex 
                  justify="center" 
                  align="center" 
                  w="full" 
                  h="full"
                  bg={item.bgColor || 'transparent'}
                  borderRadius="md"
                  p={4}
                  minH="120px"
                >
                  <Text 
                    fontSize="4xl"
                    fontWeight="bold"
                    color={item.bgColor ? 'white' : 'gray.800'}
                    _dark={{ color: item.bgColor ? 'white' : 'gray.100' }}
                    textAlign="center"
                    w="50%"
                    mx="auto"
                  >
                    {item.value}
                  </Text>
                </Flex>
              )}
            </VStack>
          ))}
        </Grid>

        {/* 吉凶事项 */}
        <Grid templateColumns="repeat(2, 1fr)" gap={4}>
          <Box 
            p={4} 
            bg="green.50" 
            _dark={{ 
              bg: 'rgba(154, 230, 180, 0.06)'  // 更柔和的绿色背景
            }}
            borderRadius="lg"
          >
            <Text 
              fontSize="6xl" 
              color="green.500" 
              _dark={{ 
                color: 'green.200'
              }}
              mb={2} 
              fontWeight="bold"
            >
              宜
            </Text>
            <VStack align="start" spacing={1}>
              {dailyFortune.activities.good.map((item, index) => (
                <Text 
                  key={index}
                  fontSize="3xl"
                  color="blackAlpha.800"
                  _dark={{ color: 'whiteAlpha.800' }}
                >
                  {item}
                </Text>
              ))}
            </VStack>
          </Box>
          <Box 
            p={4} 
            bg="red.50"
            _dark={{ 
              bg: 'rgba(254, 178, 178, 0.06)'  // 更柔和的红色背景
            }}
            borderRadius="lg"
          >
            <Text 
              fontSize="6xl" 
              color="red.500"
              _dark={{ 
                color: 'red.200'
              }}
              mb={2} 
              fontWeight="bold"
            >
              忌
            </Text>
            <VStack align="start" spacing={1}>
              {dailyFortune.activities.bad.map((item, index) => (
                <Text 
                  key={index}
                  fontSize="3xl"
                  color="blackAlpha.800"
                  _dark={{ color: 'whiteAlpha.800' }}
                >
                  {item}
                </Text>
              ))}
            </VStack>
          </Box>
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
            <Radio 
              value="profession"
              colorScheme="pink"
              size="lg"
            >
              流年分析
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
            特别想了解的问题（选填）注意：填入后选择的解析主题不再进行分析
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

      <VStack spacing={4} w="full">
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
          loadingText={`分析进度 ${Math.round(userInfo.analysisProgress || 0)}%`}
          spinner={
            <Spinner
              thickness="4px"
              speed="0.65s"
              emptyColor="whiteAlpha.300"
              color="white"
              size="md"
            />
          }
          onClick={handleAnalysis}
        >
          <VStack spacing={1}>
            <Text fontSize="lg">开启命理解析</Text>
            <Text fontSize="xs" opacity={0.9}>滴天髓深度分析</Text>
          </VStack>
        </Button>
      </VStack>
    </Container>
  )
}
