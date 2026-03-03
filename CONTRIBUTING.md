# Contributing to Kelvin Capital

Thank you for your interest in contributing! This is an open-source options trading bot, and all improvements are welcome.

## How to Contribute

### Reporting Bugs
- Check if the bug is already reported in Issues
- Include steps to reproduce
- Include error messages and logs
- Specify your environment (OS, Python version)

### Suggesting Features
- Open an Issue with the "enhancement" label
- Describe the feature and its benefits
- Explain how it fits the project goals

### Code Contributions

#### Setup
```bash
git clone https://github.com/kelvincapital/kelvin-capital.git
cd kelvin-capital
make install
```

#### Running Tests
```bash
make test
```

#### Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small

#### Pull Request Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests (`make test`)
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

### Areas Needing Help

#### High Priority
- [ ] More unit tests (aiming for 90%+ coverage)
- [ ] Integration tests with mock APIs
- [ ] Backtesting framework
- [ ] Performance optimization

#### Medium Priority
- [ ] Additional options strategies
- [ ] Web dashboard for monitoring
- [ ] Telegram/Discord bot integration
- [ ] More documentation

#### Low Priority
- [ ] Code refactoring
- [ ] Better error handling
- [ ] Logging improvements

### Questions?

Open an Issue or reach out on Twitter [@Kelvin_Capital_](https://x.com/Kelvin_Capital_)

---

**Note:** This is a paper trading project. No real money is at risk. Always test thoroughly before any live deployment.
