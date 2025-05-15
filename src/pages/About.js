import React from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const About = () => {
  const activities = [
    '파이썬 프로그래밍 기초 학습',
    '웹 개발 프로젝트',
    '게임 개발 프로젝트',
    '코딩 대회 참가',
    '해커톤 참가',
    '선배와의 멘토링',
  ];

  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="md">
        <Typography variant="h3" component="h1" gutterBottom align="center">
          코딩동아리 소개
        </Typography>
        
        <Paper sx={{ p: 4, mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            우리 동아리는
          </Typography>
          <Typography paragraph>
            이천양정여중 코딩동아리는 학생들이 프로그래밍을 배우고 실습할 수 있는
            공간입니다. 초보자부터 고급자까지 모두가 함께 성장할 수 있는 환경을
            제공합니다.
          </Typography>
          <Typography paragraph>
            우리는 단순히 코딩을 배우는 것을 넘어, 창의적인 문제 해결 능력과
            팀워크를 기르는 것을 목표로 합니다.
          </Typography>
        </Paper>

        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 4 }}>
              <Typography variant="h5" gutterBottom>
                주요 활동
              </Typography>
              <List>
                {activities.map((activity, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <CheckCircleIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={activity} />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 4 }}>
              <Typography variant="h5" gutterBottom>
                모집 안내
              </Typography>
              <Typography paragraph>
                • 모집 대상: 이천양정여중 재학생
              </Typography>
              <Typography paragraph>
                • 모집 인원: 20명
              </Typography>
              <Typography paragraph>
                • 활동 시간: 매주 화요일, 목요일 방과후
              </Typography>
              <Typography paragraph>
                • 지원 방법: 담임선생님께 문의
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default About; 