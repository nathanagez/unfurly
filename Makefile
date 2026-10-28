PYTHON_VERSION := 3.14
LAMBDA_PLATFORM := aarch64-manylinux2014

define install_dependencies
	uv export --frozen --no-default-groups $(1) --no-emit-project --no-header -o $(ARTIFACTS_DIR)/requirements.txt
	uv pip install -r $(ARTIFACTS_DIR)/requirements.txt --target $(ARTIFACTS_DIR) \
		--python-platform $(LAMBDA_PLATFORM) --python-version $(PYTHON_VERSION) --only-binary :all:
	rm $(ARTIFACTS_DIR)/requirements.txt
endef

define copy_sources
	cp -r src/$(1) src/shared $(ARTIFACTS_DIR)/
	rm -rf $(ARTIFACTS_DIR)/shared/testing
endef

build-SlackEventsFunction:
	$(call install_dependencies,)
	$(call copy_sources,api)

build-UnfurlReelFunction:
	$(call install_dependencies,--group unfurl-reel)
	$(call copy_sources,workers)

build-KillSwitchFunction:
	$(call install_dependencies,)
	$(call copy_sources,ops)
