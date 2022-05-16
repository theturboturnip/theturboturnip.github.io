initSidebarItems({"struct":[["CheriAggregateMemory","Wrapper for AggregateMemory64 that keeps tags, supports MemoryOf for reading/writing capabilities. All other Memory variants clear associated tag bits on write."],["IntegerModeCheriAggregateMemory","Wrapper for a reference to CheriAggregateMemory that allows integer-mode accesses. Exposes MemoryOf<{u8,u16,u32,u64}, TAddr=u64>."],["TagMemory","Memory holding tags for capabilities. Implements MemoryOf, which checks if the supplied address is a multiple of 16-bytes i.e. the size of a capability."]],"trait":[["CheriMemory",""]]});