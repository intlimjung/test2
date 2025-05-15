import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
} from '@mui/material';

const Projects = () => {
  const projects = [
    {
      title: '테트리스 게임',
      description: '파이썬과 Pygame을 사용하여 만든 클래식 테트리스 게임',
      image: '/images/tetris.jpg',
      tech: 'Python, Pygame',
    },
    {
      title: '포켓몬 카드 게임',
      description: '포켓몬 카드를 활용한 멀티플레이어 카드 게임',
      image: '/images/pokemon.jpg',
      tech: 'Python, Pygame',
    },
    {
      title: '동아리 웹사이트',
      description: 'React를 사용하여 만든 동아리 소개 웹사이트',
      image: '/images/website.jpg',
      tech: 'React, Material-UI',
    },
  ];

  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        <Typography variant="h3" component="h1" gutterBottom align="center">
          프로젝트 갤러리
        </Typography>
        <Typography variant="h6" align="center" color="text.secondary" paragraph>
          우리 동아리에서 진행한 다양한 프로젝트들을 소개합니다
        </Typography>

        <Grid container spacing={4} sx={{ mt: 2 }}>
          {projects.map((project, index) => (
            <Grid item key={index} xs={12} md={4}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={project.image}
                  alt={project.title}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h5" component="h2">
                    {project.title}
                  </Typography>
                  <Typography paragraph color="text.secondary">
                    {project.description}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    사용 기술: {project.tech}
                  </Typography>
                </CardContent>
                <Box sx={{ p: 2 }}>
                  <Button variant="contained" color="primary" fullWidth>
                    자세히 보기
                  </Button>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Box sx={{ mt: 6, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            새로운 프로젝트에 참여하고 싶으신가요?
          </Typography>
          <Button variant="contained" color="primary" size="large">
            동아리 가입하기
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default Projects; 