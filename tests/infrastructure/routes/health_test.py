class TestHealth:
    def test_health_success(self, client):
        response = client.get('/health')

        assert response.status_code == 200
