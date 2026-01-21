# Contributing to DevOps Task Manager

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Keep discussions on topic

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Docker version, etc.)

### Suggesting Features

1. Create an issue with the `enhancement` label
2. Describe the feature and its benefits
3. Provide use cases
4. Discuss implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/dev-ops-basit-.git
   cd dev-ops-basit-
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation

4. **Test your changes**
   ```bash
   ./scripts/test.sh
   docker-compose up -d
   # Test manually
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

   Use conventional commit messages:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test additions/changes
   - `chore:` Build/config changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description
   - Reference related issues
   - Include screenshots for UI changes

## Development Setup

```bash
# Clone repository
git clone <repo-url>
cd dev-ops-basit-

# Install dependencies
./scripts/setup.sh

# Start development environment
docker-compose up -d
```

## Coding Standards

### JavaScript/Node.js
- Use ES6+ features
- Follow Airbnb style guide
- Use async/await for async operations
- Add JSDoc comments for functions

### React
- Use functional components with hooks
- Keep components small and focused
- Use meaningful variable names
- Add PropTypes or TypeScript

### Docker
- Use multi-stage builds
- Minimize image size
- Don't run as root
- Use specific version tags

### Kubernetes
- Follow naming conventions
- Add resource limits
- Include health checks
- Use namespaces

## Testing

### Backend Tests
```bash
cd backend
npm test
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
docker-compose up -d
# Run integration tests
```

## Documentation

- Update README.md for major changes
- Add API documentation for new endpoints
- Update deployment guides
- Include inline code comments

## Review Process

1. Automated checks must pass
   - Linting
   - Tests
   - Security scans
   - Build verification

2. Code review by maintainers
   - Code quality
   - Test coverage
   - Documentation
   - Performance impact

3. Approval and merge

## Areas for Contribution

### Features
- [ ] User authentication
- [ ] Task categories
- [ ] Due dates
- [ ] Task priorities
- [ ] Search functionality
- [ ] Dark mode

### DevOps
- [ ] Helm charts
- [ ] Ansible playbooks
- [ ] GitLab CI/CD
- [ ] Jenkins pipeline
- [ ] ArgoCD configuration

### Testing
- [ ] E2E tests
- [ ] Load testing
- [ ] Security testing
- [ ] Chaos engineering

### Documentation
- [ ] Video tutorials
- [ ] Architecture diagrams
- [ ] Best practices guide
- [ ] Troubleshooting guide

## Questions?

Feel free to:
- Open an issue for discussion
- Join our community chat
- Email the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
